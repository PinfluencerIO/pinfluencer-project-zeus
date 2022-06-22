import base64
import io
import os
import uuid
from typing import Callable, Union

import boto3
from botocore.exceptions import ClientError
from filetype import filetype

from src.data.entities import SqlAlchemyBrandEntity, SqlAlchemyInfluencerEntity, create_mappings
from src.domain.models import Brand, Influencer
from src.domain.models import User as UserModel
from src.exceptions import AlreadyExistsException, ImageException, NotFoundException
from src.types import DataManager, ImageRepository, Model, User, ObjectMapperAdapter


class BaseSqlAlchemyRepository:
    def __init__(self,
                 data_manager: DataManager,
                 resource_entity,
                 object_mapper: ObjectMapperAdapter,
                 resource_dto):
        self._object_mapper = object_mapper
        self._data_manager = data_manager
        self._resource_entity = resource_entity
        self._resource_dto = resource_dto

        create_mappings(mapper=self._object_mapper)

    def load_collection(self) -> list[Model]:
        return list(map(lambda x: self._object_mapper.map(from_obj=x, to_type=self._resource_dto),
                        self._data_manager.session.query(self._resource_entity).all()))

    def load_by_id(self, id_) -> Model:
        entity = self._data_manager.session.query(self._resource_entity).filter(self._resource_entity.id == id_).first()
        if entity:
            return self._object_mapper.map(from_obj=entity, to_type=self._resource_dto)
        else:
            raise NotFoundException(f'model {id} was not found')


class BaseSqlAlchemyUserRepository(BaseSqlAlchemyRepository):
    def __init__(self, data_manager: DataManager,
                 resource_entity,
                 image_repository: ImageRepository,
                 object_mapper: ObjectMapperAdapter,
                 resource_dto):
        super().__init__(data_manager=data_manager,
                         resource_entity=resource_entity,
                         object_mapper=object_mapper,
                         resource_dto=resource_dto)
        self.__image_repository = image_repository

    def load_for_auth_user(self, auth_user_id) -> User:
        first = self._data_manager.session \
            .query(self._resource_entity) \
            .filter(self._resource_entity.auth_user_id == auth_user_id) \
            .first()
        if first:
            return self._object_mapper.map(from_obj=first, to_type=self._resource_dto)
        raise NotFoundException(f'user {auth_user_id} not found')

    def write_new_for_auth_user(self, auth_user_id, payload) -> User:
        try:
            entity = self.load_for_auth_user(auth_user_id)
            raise AlreadyExistsException(f'{self._resource_entity.__name__}'
                                         f'{entity.id} already associated with {auth_user_id}')
        except NotFoundException:
            try:
                payload.auth_user_id = auth_user_id
                entity = self._object_mapper.map(from_obj=payload, to_type=self._resource_entity)
                self._data_manager.session.add(entity)
                self._data_manager.session.commit()
                return self._object_mapper.map(from_obj=entity, to_type=self._resource_dto)
            except Exception as e:
                print(f'Failed to write_new_{self._resource_entity.__class__.__name__}_for_auth_user {e}')
                self._data_manager.session.rollback()
                raise e

    def _update_image(self, auth_user_id, image_bytes, field_setter: Callable[[str, User], None]):
        user = self._data_manager.session.query(self._resource_entity).filter(
            self._resource_entity.auth_user_id == auth_user_id).first()
        if user:
            image = self.__image_repository.upload(path=user.id,
                                                   image_base64_encoded=image_bytes)
            print(f'setting user {auth_user_id} image to {image}')
            field_setter(image, user)
            self._data_manager.session.commit()
            print(
                f'Repository Event: user after image set \n{self._object_mapper.map(from_obj=user, to_type=self._resource_dto).__dict__}')
            first = self._data_manager.session \
                .query(self._resource_entity) \
                .filter(self._resource_entity.auth_user_id == auth_user_id) \
                .first()
            return self._object_mapper.map(from_obj=first, to_type=self._resource_dto)
        else:
            raise NotFoundException(f'brand {auth_user_id} could not be found')


class SqlAlchemyBrandRepository(BaseSqlAlchemyUserRepository):
    def __init__(self,
                 data_manager: DataManager,
                 image_repository: ImageRepository,
                 object_mapper: Union[object, ObjectMapperAdapter]):
        super().__init__(data_manager=data_manager,
                         resource_entity=SqlAlchemyBrandEntity,
                         image_repository=image_repository,
                         object_mapper=object_mapper,
                         resource_dto=Brand)

    def update_for_auth_user(self, auth_user_id, payload: Brand) -> Brand:
        entity = self._data_manager.session.query(self._resource_entity).filter(
            self._resource_entity.auth_user_id == auth_user_id).first()
        if entity:
            entity.brand_name = payload.brand_name
            entity.brand_description = payload.brand_description
            entity.insta_handle = payload.insta_handle
            entity.values = payload.values
            entity.categories = payload.categories
            entity.website = payload.website
            self._data_manager.session.commit()
            return self._object_mapper.map(from_obj=entity, to_type=self._resource_dto)
        else:
            raise NotFoundException(f'brand {auth_user_id} not found')

    def update_logo_for_auth_user(self, auth_user_id, image_bytes) -> Brand:
        return self._update_image(auth_user_id=auth_user_id,
                                  image_bytes=image_bytes,
                                  field_setter=self.__logo_setter)

    def update_header_image_for_auth_user(self, auth_user_id, image_bytes) -> Brand:
        return self._update_image(auth_user_id=auth_user_id,
                                  image_bytes=image_bytes,
                                  field_setter=self.__header_image_setter)

    @staticmethod
    def __logo_setter(logo, brand):
        brand.logo = logo

    @staticmethod
    def __header_image_setter(header_image, brand):
        brand.header_image = header_image


class SqlAlchemyInfluencerRepository(BaseSqlAlchemyUserRepository):
    def __init__(self,
                 data_manager: DataManager,
                 image_repository: ImageRepository,
                 object_mapper: Union[object, ObjectMapperAdapter]):
        super().__init__(data_manager=data_manager,
                         resource_entity=SqlAlchemyInfluencerEntity,
                         image_repository=image_repository,
                         object_mapper=object_mapper,
                         resource_dto=Influencer)

    def update_for_auth_user(self, auth_user_id: str, payload: Influencer) -> Influencer:
        ...

    def update_image_for_auth_user(self, auth_user_id: str, image_bytes: str) -> Influencer:
        ...


class S3ImageRepository:

    def __init__(self):
        self.__bucket_name = 'pinfluencer-product-images'
        self.__s3_client = boto3.client('s3')

    def upload(self, path, image_base64_encoded):
        image = base64.b64decode(image_base64_encoded)
        f = io.BytesIO(image)
        file_type = filetype.guess(f)
        print(f'image uploading to {path}/ of {file_type}')
        if file_type is not None:
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
        self.__client = boto3.client('cognito-idp')

    def update_user_claims(self, username: str, attributes: list[dict]) -> None:
        self.__client.admin_update_user_attributes(
            UserPoolId=os.environ["USER_POOL_ID"],
            Username=username,
            UserAttributes=attributes
        )

    def get_user(self, username: str) -> dict:
        return self.__client.admin_get_user(
            UserPoolId='string',
            Username='string'
        )


class CognitoAuthUserRepository:

    def __init__(self, auth_service: CognitoAuthService):
        self.__auth_service = auth_service

    def get_by_id(self, _id: str) -> User:
        auth_user = self.__auth_service.get_user(username=_id)
        first_name = self.__get_cognito_attribute(user=auth_user,
                                                  attribute_name='given_name')
        last_name = self.__get_cognito_attribute(user=auth_user,
                                                 attribute_name='family_name')
        email = self.__get_cognito_attribute(user=auth_user,
                                             attribute_name='email')
        return UserModel(first_name=first_name,
                         last_name=last_name,
                         email=email)

    def __get_cognito_attribute(self, user: dict, attribute_name: str) -> str:
        return next(filter(lambda x: x['Name'] == attribute_name, user['UserAttributes']))['Value']

    def update_brand_claims(self, user: Brand):
        self.__update_user_claims(user=user, type='brand')

    def update_influencer_claims(self, user: Influencer):
        self.__update_user_claims(user=user, type='influencer')

    def __update_user_claims(self, user: User, type: str):
        self.__auth_service.update_user_claims(username=user.auth_user_id, attributes=[
            {
                'Name': 'custom:type',
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
