import base64
import io
import json
import uuid
from typing import Callable

import boto3
from botocore.exceptions import ClientError
from filetype import filetype

from src.data.entities import BrandEntity, InfluencerEntity
from src.domain.models import Brand
from src.exceptions import AlreadyExistsException, ImageException, NotFoundException
from src.types import DataManager, ImageRepository, Model, User


class BaseSqlAlchemyRepository:
    def __init__(self, data_manager: DataManager, resource):
        self._data_manager = data_manager
        self._resource = resource

    def load_collection(self) -> list[Model]:
        return list(map(lambda x: x.as_dto(), self._data_manager.session.query(self._resource).all()))

    def load_by_id(self, id_) -> Model:
        entity = self._data_manager.session.query(self._resource).filter(self._resource.id == id_).first()
        if entity:
            return entity.as_dto()
        else:
            raise NotFoundException(f'model {id} was not found')


class BaseSqlAlchemyUserRepository(BaseSqlAlchemyRepository):
    def __init__(self, data_manager, resource, image_repository):
        super().__init__(data_manager, resource)
        self.__image_repository = image_repository

    def load_for_auth_user(self, auth_user_id) -> User:
        first = self._data_manager.session \
            .query(self._resource) \
            .filter(self._resource.auth_user_id == auth_user_id) \
            .first()
        if first:
            return first.as_dto()
        raise NotFoundException(f'user {auth_user_id} not found')

    def write_new_for_auth_user(self, auth_user_id, payload) -> User:
        try:
            entity = self.load_for_auth_user(auth_user_id)
            raise AlreadyExistsException(f'{self._resource.__name__}'
                                         f'{entity.id} already associated with {auth_user_id}')
        except NotFoundException:
            try:
                payload.auth_user_id = auth_user_id
                entity = self._resource.create_from_dto_without_images(dto=payload)
                self._data_manager.session.add(entity)
                self._data_manager.session.commit()
                return entity
            except Exception as e:
                print(f'Failed to write_new_{self._resource.__class__.__name__}_for_auth_user {e}')
                self._data_manager.session.rollback()
                raise e

    def _update_image(self, auth_user_id, image_bytes, field_setter: Callable[[str, User], None]):
        user = self._data_manager.session.query(self._resource).filter(
            self._resource.auth_user_id == auth_user_id).first()
        if user:
            image = self.__image_repository.upload(path=user.id,
                                                   image_base64_encoded=image_bytes)
            print(f'setting user {auth_user_id} image to {image}')
            field_setter(image, user)
            self._data_manager.session.commit()
            print(f'Repository Event: user after image set \n{user.as_dto().__dict__}')
            return user.as_dto()
        else:
            raise NotFoundException(f'brand {auth_user_id} could not be found')


class SqlAlchemyBrandRepository(BaseSqlAlchemyUserRepository):
    def __init__(self,
                 data_manager: DataManager,
                 image_repository: ImageRepository):
        super().__init__(data_manager=data_manager,
                         resource=BrandEntity,
                         image_repository=image_repository)

    def update_for_auth_user(self, auth_user_id, payload: Brand) -> Brand:
        entity = self._data_manager.session.query(self._resource).first()
        if entity:
            entity.first_name = payload.first_name
            entity.last_name = payload.last_name
            entity.email = payload.email
            entity.name = payload.name
            entity.description = payload.description
            entity.instahandle = payload.instahandle
            entity.values = json.dumps(list(map(lambda x: x.name, payload.values)))
            entity.categories = json.dumps(list(map(lambda x: x.name, payload.categories)))
            entity.website = payload.website
            self._data_manager.session.commit()
            return entity.as_dto()
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
                 image_repository: ImageRepository):
        super().__init__(data_manager=data_manager,
                         resource=InfluencerEntity,
                         image_repository=image_repository)


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
            return file
        except ClientError:
            raise ImageException
