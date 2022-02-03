import base64
import io
import json
import uuid

import boto3
from botocore.exceptions import ClientError
from filetype import filetype

from src.data.entities import BrandEntity, InfluencerEntity
from src.domain.models import Brand
from src.exceptions import AlreadyExistsException, ImageException
from src.types import DataManager


class BaseSqlAlchemyRepository:
    def __init__(self, data_manager: DataManager, resource):
        self._data_manager = data_manager
        self._resource = resource

    def load_collection(self):
        return list(map(lambda x: x.as_dto(), self._data_manager.session.query(self._resource).all()))

    def load_by_id(self, id_):
        entity = self._data_manager.session.query(self._resource).filter(self._resource.id == id_).first()
        if entity:
            return entity.as_dto()
        else:
            return None


class BaseSqlAlchemyUserRepository(BaseSqlAlchemyRepository):
    def __init__(self, data_manager, resource):
        super().__init__(data_manager, resource)

    def load_for_auth_user(self, auth_user_id):
        first = self._data_manager.session\
            .query(self._resource)\
            .filter(self._resource.auth_user_id == auth_user_id)\
            .first()
        if first:
            return first.as_dto()
        return None

    def write_new_for_auth_user(self, auth_user_id, payload):
        entity = self.load_for_auth_user(auth_user_id)
        if entity:
            raise AlreadyExistsException(f'{self._resource.__name__}'
                                         f'{entity.id} already associated with {auth_user_id}')
        else:
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
    def __init__(self, data_manager):
        super().__init__(data_manager=data_manager, resource=BrandEntity)

    def update_for_auth_user(self, auth_user_id, payload: Brand):
        entity = self._data_manager.session.query(self._resource).first()
        entity.first_name = payload.first_name
        entity.last_name = payload.last_name
        entity.email = payload.email
        entity.name = payload.name
        entity.description = payload.description
        entity.values = json.dumps(list(map(lambda x: x.name, payload.values)))
        entity.categories = json.dumps(list(map(lambda x: x.name, payload.categories)))
        entity.website = payload.website
        self._data_manager.session.commit()


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

    def delete(self, path):
        try:
            self.__s3_client.delete_object(Bucket=self.__bucket_name, Key=path)
        except ClientError:
            raise ImageException

    def retrieve(self, path):
        try:
            image_object = self.__s3_client.get_object(self.__bucket_name, path)
            return json.loads(image_object['Body'].read())
        except ClientError:
            raise ImageException
