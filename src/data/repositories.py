import base64
import io
import os
import uuid
from typing import Type, TypeVar, Callable

import boto3
from botocore.exceptions import ClientError, ParamValidationError
from filetype import filetype

from src._types import DataManager, ImageRepository, Model, UserModel, Logger
from src.data.entities import create_mappings
from src.domain.models import Brand, Influencer, Listing, User, Notification, AudienceAgeSplit, AudienceAge, \
    AudienceGenderSplit, AudienceGender
from src.exceptions import AlreadyExistsException, ImageException, NotFoundException

TPayload = TypeVar("TPayload")
TParent = TypeVar("TParent")


class BaseSqlAlchemyRepository:
    def __init__(self,
                 data_manager: DataManager,
                 model,
                 logger: Logger):
        self._logger = logger
        self._data_manager = data_manager
        self._model = model

        create_mappings(logger=self._logger)

    def load_collection(self) -> list[Model]:
        return self._data_manager.session.query(self._model).all()

    def load_by_id(self, id_) -> Model:
        entity = self._data_manager.session.query(self._model).filter(self._model.id == id_).first()
        if entity:
            return entity
        else:
            raise NotFoundException(f'model {id} was not found')

    def save(self):
        self._logger.log_debug("starting commit ...")
        self._data_manager.session.flush()
        self._data_manager.session.commit()
        self._logger.log_debug("status committed ...")


class BaseSqlAlchemyOwnerRepository(BaseSqlAlchemyRepository):

    def __init__(self, data_manager: DataManager,
                 model,
                 logger: Logger):
        super().__init__(data_manager=data_manager,
                         model=model,
                         logger=logger)

    def _write_new_for_owner(self,
                             payload: TPayload,
                             foreign_key_setter: Callable[[TPayload], None]) -> TPayload:
        foreign_key_setter(payload)
        self._data_manager.session.add(payload)
        return payload

    def _load_for_auth_owner(self,
                             auth_user_id: str,
                             model: Type[TPayload],
                             model_entity_field) -> list[TPayload]:
        children = self._data_manager \
            .session \
            .query(model) \
            .filter(model_entity_field == auth_user_id) \
            .all()
        return children


class BaseSqlAlchemyUserRepository(BaseSqlAlchemyRepository):
    def __init__(self, data_manager: DataManager,
                 model,
                 image_repository: ImageRepository,
                 logger: Logger):
        super().__init__(data_manager=data_manager,
                         model=model,
                         logger=logger)

    def load_for_auth_user(self, auth_user_id) -> UserModel:
        self._logger.log_debug(f"query load for auth user for {self._model.__name__}")
        first = self._data_manager.session \
            .query(self._model) \
            .filter(self._model.auth_user_id == auth_user_id) \
            .first()
        if first:
            return first
        raise NotFoundException(f'user {auth_user_id} not found')

    def write_new_for_auth_user(self, auth_user_id, payload: UserModel) -> UserModel:
        try:
            self._logger.log_debug(f"write for auth user for {self._model.__name__}")
            entity = self.load_for_auth_user(auth_user_id)
            raise AlreadyExistsException(f'{self._model.__name__}'
                                         f'{entity.id} already associated with {auth_user_id}')
        except NotFoundException:
            try:
                payload.auth_user_id = auth_user_id
                self._data_manager.session.add(payload)
                return payload
            except Exception as e:
                self._logger.log_error(f"failed to write for auth user for {self._model.__name__}")
                raise e


class SqlAlchemyAudienceAgeRepository(BaseSqlAlchemyOwnerRepository):

    def __init__(self, data_manager: DataManager,
                 logger: Logger):
        super().__init__(data_manager,
                         Listing,
                         logger=logger)

    def write_new_for_influencer(self,
                                 payload: AudienceAgeSplit,
                                 auth_user_id: str) -> AudienceAgeSplit:
        for audience_age in payload.audience_ages:
            self._write_new_for_owner(payload=audience_age,
                                      foreign_key_setter=lambda x:
                                      self.__set_audience_age_auth_user_id(audience_age=x,
                                                                           auth_user_id=auth_user_id))
        return payload

    def load_for_influencer(self,
                            auth_user_id: str) -> AudienceAgeSplit:
        return \
            AudienceAgeSplit(audience_ages=self._load_for_auth_owner(auth_user_id=auth_user_id,
                                                                     model_entity_field=AudienceAge.influencer_auth_user_id,
                                                                     model=AudienceAge))

    def __set_audience_age_auth_user_id(self, audience_age: AudienceAge, auth_user_id: str):
        audience_age.influencer_auth_user_id = auth_user_id


class SqlAlchemyAudienceGenderRepository(BaseSqlAlchemyOwnerRepository):

    def __init__(self, data_manager: DataManager,
                 logger: Logger):
        super().__init__(data_manager,
                         Listing,
                         logger=logger)

    def write_new_for_influencer(self,
                                 payload: AudienceGenderSplit,
                                 auth_user_id: str) -> AudienceGenderSplit:
        for audience_age in payload.audience_genders:
            self._write_new_for_owner(payload=audience_age,
                                      foreign_key_setter=lambda x:
                                      self.__set_audience_gender_auth_user_id(audience_age=x,
                                                                              auth_user_id=auth_user_id))
        return payload

    def load_for_influencer(self,
                            auth_user_id: str) -> AudienceGenderSplit:
        return \
            AudienceGenderSplit(audience_genders=self._load_for_auth_owner(auth_user_id=auth_user_id,
                                                                           model_entity_field=AudienceGender.influencer_auth_user_id,
                                                                           model=AudienceGender))

    def __set_audience_gender_auth_user_id(self, audience_age: AudienceGender, auth_user_id: str):
        audience_age.influencer_auth_user_id = auth_user_id


class SqlAlchemyBrandRepository(BaseSqlAlchemyUserRepository):
    def __init__(self,
                 data_manager: DataManager,
                 image_repository: ImageRepository,
                 logger: Logger):
        super().__init__(data_manager=data_manager,
                         model=Brand,
                         image_repository=image_repository,
                         logger=logger)


class SqlAlchemyInfluencerRepository(BaseSqlAlchemyUserRepository):
    def __init__(self,
                 data_manager: DataManager,
                 image_repository: ImageRepository,
                 logger: Logger):
        super().__init__(data_manager=data_manager,
                         model=Influencer,
                         image_repository=image_repository,
                         logger=logger)


class SqlAlchemyListingRepository(BaseSqlAlchemyOwnerRepository):

    def __init__(self, data_manager: DataManager,
                 image_repository: ImageRepository,
                 logger: Logger):
        super().__init__(data_manager,
                         Listing,
                         logger=logger)

    def write_new_for_brand(self,
                            payload: Listing,
                            auth_user_id: str) -> Listing:
        return self._write_new_for_owner(payload=payload,
                                         foreign_key_setter=lambda x: self.__brand_auth_user_id_setter(payload=x,
                                                                                                       auth_user_id=auth_user_id))

    def __brand_auth_user_id_setter(self, payload: Listing, auth_user_id: str):
        payload.brand_auth_user_id = auth_user_id

    def load_for_auth_brand(self, auth_user_id: str) -> list[Listing]:
        return self._load_for_auth_owner(auth_user_id=auth_user_id,
                                         model_entity_field=Listing.brand_auth_user_id,
                                         model=Listing)


class SqlAlchemyNotificationRepository(BaseSqlAlchemyRepository):

    def __init__(self, data_manager: DataManager,
                 logger: Logger):
        super().__init__(data_manager,
                         Notification,
                         logger=logger)

    def write_new_for_auth_user(self, auth_user_id: str, payload: Notification) -> Notification:
        self._data_manager.session.add(payload)
        return payload


class S3ImageRepository:

    def __init__(self, logger: Logger):
        self.__logger = logger
        self.__bucket_name = 'pinfluencer-product-images'
        self.__s3_client = boto3.client('s3')

    def upload(self, path, image_base64_encoded):
        self.__logger.log_trace(f"uploading image to S3 repo {image_base64_encoded}")
        image = base64.b64decode(image_base64_encoded)
        f = io.BytesIO(image)
        file_type = filetype.get_type(ext='jpg')
        try:
            file_type = filetype.guess(f)
        except Exception:
            ...
        self.__logger.log_debug(f'image uploading to {path}/ of {file_type}')
        if file_type is not None:
            self.__logger.log_trace(f"file type {file_type}")
            mime = file_type.MIME
        else:
            mime = 'image/jpg'
        image_id = str(uuid.uuid4())
        file = f'{image_id}.{file_type.EXTENSION}'
        self.__logger.log_trace(f'image {file}')
        key = f'{path}/{file}'
        self.__logger.log_trace(f'key {key}')
        try:
            self.__s3_client.put_object(Bucket=self.__bucket_name,
                                        Key=key, Body=image,
                                        ContentType=mime,
                                        Tagging='public=yes')
            return key
        except ClientError:
            raise ImageException


class CognitoAuthService:

    def __init__(self, logger: Logger):
        self.__logger = logger
        self.__logger.log_trace(f"user pool id: {os.environ['USER_POOL_ID']}")
        self.__client = boto3.client('cognito-idp')

    def update_user_claims(self, username: str, attributes: list[dict]) -> None:
        self.__client.admin_update_user_attributes(
            UserPoolId=os.environ["USER_POOL_ID"],
            Username=username,
            UserAttributes=attributes
        )

    def get_user(self, username: str) -> dict:
        self.__logger.log_trace(f"username is {username}")
        self.__logger.log_trace(f"userpool is {os.environ['USER_POOL_ID']}")
        return self.__client.admin_get_user(
            UserPoolId=os.environ["USER_POOL_ID"],
            Username=username
        )


class CognitoAuthUserRepository:

    def __init__(self, auth_service: CognitoAuthService,
                 logger: Logger):
        self.__logger = logger
        self.__auth_service = auth_service

    def get_by_id(self, _id: str) -> User:
        self.__logger.log_trace(f"username is {_id}")
        auth_user = self.__auth_service.get_user(username=_id)
        first_name = self.__get_cognito_attribute(user=auth_user,
                                                  attribute_name='given_name')
        last_name = self.__get_cognito_attribute(user=auth_user,
                                                 attribute_name='family_name')
        email = self.__get_cognito_attribute(user=auth_user,
                                             attribute_name='email')
        return User(given_name=first_name,
                    family_name=last_name,
                    email=email)

    def __get_cognito_attribute(self, user: dict, attribute_name: str) -> str:
        return next(filter(lambda x: x['Name'] == attribute_name, user['UserAttributes']))['Value']

    def update_brand_claims(self, user: User, auth_user_id: str):
        self._update_user_claims(user=user, type='brand',
                                 auth_user_id=auth_user_id)

    def update_influencer_claims(self, user: User, auth_user_id: str):
        self._update_user_claims(user=user, type='influencer',
                                 auth_user_id=auth_user_id)

    def _update_user_claims(self, user: User, type: str, auth_user_id: str):
        try:
            list_of_attributes = self.__flexi_update_claims(user=user)
            list_of_attributes.append({
                'Name': 'custom:usertype',
                'Value': type
            })
            self.__auth_service.update_user_claims(username=auth_user_id, attributes=list_of_attributes)
        except ParamValidationError:
            ...

    def __flexi_update_claims(self, user: User) -> list[dict]:
        attributes = []
        values = vars(user).items()
        for key, value in values:
            try:
                value_in_request = getattr(user, key)
                if value_in_request is not None:
                    attributes.append({
                        "Name": key,
                        "Value": value
                    })
            except AttributeError:
                ...
        return attributes
