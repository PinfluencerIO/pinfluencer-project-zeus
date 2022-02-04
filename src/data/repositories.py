import base64
import io
import json
import uuid

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
    def __init__(self, data_manager, resource):
        super().__init__(data_manager, resource)

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


class SqlAlchemyBrandRepository(BaseSqlAlchemyUserRepository):
    def __init__(self, data_manager, image_repository: ImageRepository):
        super().__init__(data_manager=data_manager, resource=BrandEntity)
        self.__image_repository = image_repository

    def update_for_auth_user(self, auth_user_id, payload: Brand) -> Brand:
        entity = self._data_manager.session.query(self._resource).first()
        if entity:
            entity.first_name = payload.first_name
            entity.last_name = payload.last_name
            entity.email = payload.email
            entity.name = payload.name
            entity.description = payload.description
            entity.values = json.dumps(list(map(lambda x: x.name, payload.values)))
            entity.categories = json.dumps(list(map(lambda x: x.name, payload.categories)))
            entity.website = payload.website
            self._data_manager.session.commit()
            return entity.as_dto()
        else:
            raise NotFoundException(f'brand {auth_user_id} not found')

    def update_logo_for_auth_user(self, auth_user_id, image_bytes) -> Brand:
        brand = self._data_manager.session.query(BrandEntity).filter(BrandEntity.auth_user_id == auth_user_id).first()
        if brand:
            image = self.__image_repository.upload(path=brand.id, image_base64_encoded=image_bytes)
            brand.logo = image
            self._data_manager.session.commit()
            return brand.as_dto()
        else:
            raise NotFoundException(f'brand {auth_user_id} could not be found')

    def update_header_image_for_auth_user(self, auth_user_id, image_bytes) -> Brand:
        brand = self._data_manager.session.query(BrandEntity).filter(BrandEntity.auth_user_id == auth_user_id).first()
        if brand:
            image = self.__image_repository.upload(path=brand.id, image_base64_encoded=image_bytes)
            brand.header_image = image
            self._data_manager.session.commit()
            return brand.as_dto()
        else:
            raise NotFoundException(f'brand {auth_user_id} could not be found')


class SqlAlchemyInfluencerRepository(BaseSqlAlchemyUserRepository):
    def __init__(self, data_manager):
        super().__init__(data_manager=data_manager, resource=InfluencerEntity)


class S3ImageRepository:

    def __init__(self):
        self.__bucket_name = 'pinfluencer-product-images'
        self.__s3_client = boto3.client('s3')

    def upload(self, path, image_base64_encoded):
        image = base64.b64decode(image_base64_encoded)
        f = io.BytesIO(image)
        file_type = filetype.guess(f)
        if file_type is not None:
            mime = file_type.MIME
        else:
            mime = 'image/jpg'
        image_id = str(uuid.uuid4())
        file = f'{image_id}.{file_type.EXTENSION}'
        key = f'{path}/{file}'
        try:
            self.__s3_client.put_object(Bucket=self.__bucket_name,
                                        Key=key, Body=image,
                                        ContentType=mime,
                                        Tagging='public=yes')
            return key
        except ClientError:
            raise ImageException
