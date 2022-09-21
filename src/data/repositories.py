import base64
import io
import os
import uuid

import boto3
from botocore.exceptions import ClientError, ParamValidationError
from filetype import filetype

from src._types import DataManager, ImageRepository, Model, ObjectMapperAdapter, UserModel
from src.data.entities import create_mappings
from src.domain.models import Brand, Influencer, Campaign, User
from src.exceptions import AlreadyExistsException, ImageException, NotFoundException


class BaseSqlAlchemyRepository:
    def __init__(self,
                 data_manager: DataManager,
                 model,
                 object_mapper: ObjectMapperAdapter,
                 image_repository: ImageRepository):
        self._image_repository = image_repository
        self._object_mapper = object_mapper
        self._data_manager = data_manager
        self._model = model

        create_mappings(mapper=self._object_mapper)

    def load_collection(self) -> list[Model]:
        return self._data_manager.session.query(self._model).all()

    def load_by_id(self, id_) -> Model:
        entity = self._data_manager.session.query(self._model).filter(self._model.id == id_).first()
        if entity:
            return entity
        else:
            raise NotFoundException(f'model {id} was not found')

    def save(self):
        print("status committing")
        self._data_manager.session.flush()
        self._data_manager.session.commit()
        print("status committed")


class BaseSqlAlchemyUserRepository(BaseSqlAlchemyRepository):
    def __init__(self, data_manager: DataManager,
                 model,
                 image_repository: ImageRepository,
                 object_mapper: ObjectMapperAdapter):
        super().__init__(data_manager=data_manager,
                         model=model,
                         object_mapper=object_mapper,
                         image_repository=image_repository)

    def load_for_auth_user(self, auth_user_id) -> UserModel:
        print(f"QUERY: <load for auth user> ENTITY: {self._model.__name__}")
        first = self._data_manager.session \
            .query(self._model) \
            .filter(self._model.auth_user_id == auth_user_id) \
            .first()
        if first:
            return first
        raise NotFoundException(f'user {auth_user_id} not found')

    def write_new_for_auth_user(self, auth_user_id, payload: UserModel) -> UserModel:
        try:
            entity = self.load_for_auth_user(auth_user_id)
            raise AlreadyExistsException(f'{self._model.__name__}'
                                         f'{entity.id} already associated with {auth_user_id}')
        except NotFoundException:
            try:
                payload.auth_user_id = auth_user_id
                self._data_manager.session.add(payload)
                print(f"{payload} from data.write_new_for_auth_user")
                return payload
            except Exception as e:
                print(f'Failed to write_new_{self._model.__class__.__name__}_for_auth_user {e}')
                raise e


class SqlAlchemyBrandRepository(BaseSqlAlchemyUserRepository):
    def __init__(self,
                 data_manager: DataManager,
                 image_repository: ImageRepository,
                 object_mapper: ObjectMapperAdapter):
        super().__init__(data_manager=data_manager,
                         model=Brand,
                         image_repository=image_repository,
                         object_mapper=object_mapper)


class SqlAlchemyInfluencerRepository(BaseSqlAlchemyUserRepository):
    def __init__(self,
                 data_manager: DataManager,
                 image_repository: ImageRepository,
                 object_mapper: ObjectMapperAdapter):
        super().__init__(data_manager=data_manager,
                         model=Influencer,
                         image_repository=image_repository,
                         object_mapper=object_mapper)


class SqlAlchemyCampaignRepository(BaseSqlAlchemyRepository):

    def __init__(self, data_manager: DataManager,
                 object_mapper: ObjectMapperAdapter,
                 image_repository: ImageRepository):
        super().__init__(data_manager,
                         Campaign,
                         object_mapper,
                         image_repository=image_repository)

    def write_new_for_brand(self, payload: Campaign,
                            auth_user_id: str) -> Campaign:
        brand = self._data_manager \
            .session \
            .query(Brand) \
            .filter(Brand.auth_user_id == auth_user_id) \
            .first()
        if brand:
            payload.brand_id = brand.id
            self._data_manager.session.add(payload)
            return payload
        else:
            error_message = f"brand <{auth_user_id}> not found"
            print(error_message)
            raise NotFoundException(error_message)

    def load_for_auth_brand(self, auth_user_id: str) -> list[Campaign]:
        brand = self._data_manager \
            .session \
            .query(Brand) \
            .filter(Brand.auth_user_id == auth_user_id) \
            .first()
        if brand != None:
            campaigns = self._data_manager \
                .session \
                .query(Campaign) \
                .filter(Campaign.brand_id == brand.id) \
                .all()
            return campaigns
        else:
            raise NotFoundException("brand not found")


class S3ImageRepository:

    def __init__(self):
        self.__bucket_name = 'pinfluencer-product-images'
        self.__s3_client = boto3.client('s3')

    def upload(self, path, image_base64_encoded):
        print(f"uploading image to S3 repo {image_base64_encoded}")
        image = base64.b64decode(image_base64_encoded)
        print(f"uploading image to S3 repo bytes64 encoded {image}")
        f = io.BytesIO(image)
        print(f"bytesIO file {f}")
        file_type = filetype.get_type(ext='jpg')
        try:
            file_type = filetype.guess(f)
        except Exception:
            ...
        print(f'image uploading to {path}/ of {file_type}')
        if file_type is not None:
            print(f"file type {file_type}")
            mime = file_type.MIME
        else:
            mime = 'image/jpg'
        image_id = str(uuid.uuid4())
        file = f'{image_id}.{file_type.EXTENSION}'
        print(f'image {file}')
        key = f'{path}/{file}'
        print(f'key {key}')
        try:
            self.__s3_client.put_object(Bucket=self.__bucket_name,
                                        Key=key, Body=image,
                                        ContentType=mime,
                                        Tagging='public=yes')
            return key
        except ClientError:
            raise ImageException


class CognitoAuthService:

    def __init__(self):
        print(f"user pool id: {os.environ['USER_POOL_ID']}")
        self.__client = boto3.client('cognito-idp')

    def update_user_claims(self, username: str, attributes: list[dict]) -> None:
        self.__client.admin_update_user_attributes(
            UserPoolId=os.environ["USER_POOL_ID"],
            Username=username,
            UserAttributes=attributes
        )

    def get_user(self, username: str) -> dict:
        print(f"username is {username}")
        print(f"userpool is {os.environ['USER_POOL_ID']}")
        return self.__client.admin_get_user(
            UserPoolId=os.environ["USER_POOL_ID"],
            Username=username
        )


class CognitoAuthUserRepository:

    def __init__(self, auth_service: CognitoAuthService):
        self.__auth_service = auth_service

    def get_by_id(self, _id: str) -> User:
        print(f"username is {_id}")
        auth_user = self.__auth_service.get_user(username=_id)
        first_name = self.__get_cognito_attribute(user=auth_user,
                                                  attribute_name='given_name')
        last_name = self.__get_cognito_attribute(user=auth_user,
                                                 attribute_name='family_name')
        email = self.__get_cognito_attribute(user=auth_user,
                                             attribute_name='email')
        return User(first_name=first_name,
                         last_name=last_name,
                         email=email)

    def __get_cognito_attribute(self, user: dict, attribute_name: str) -> str:
        return next(filter(lambda x: x['Name'] == attribute_name, user['UserAttributes']))['Value']

    def update_brand_claims(self, user: User):
        self.__update_user_claims(user=user, type='brand')

    def update_influencer_claims(self, user: User):
        self.__update_user_claims(user=user, type='influencer')

    def __update_user_claims(self, user: User, type: str):
        try:
            self.__auth_service.update_user_claims(username=user.auth_user_id, attributes=[
                {
                    'Name': 'custom:usertype',
                    'Value': type
                },
                {
                    'Name': 'email',
                    'Value': user.email
                },
                {
                    'Name': 'family_name',
                    'Value': user.last_name
                },
                {
                    'Name': 'given_name',
                    'Value': user.first_name
                }
            ])
        except ParamValidationError:
            ...
