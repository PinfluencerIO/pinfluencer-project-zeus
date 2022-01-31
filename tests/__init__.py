import uuid
from collections import OrderedDict
from datetime import datetime
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data_access_layer.entities import BrandEntity, Base
from src.data_access_layer.models import Brand
from src.data_access_layer.product import Product


def brand_generator(dto):
    return BrandEntity.create_from_dto(dto=dto)


def brand_dto_generator(num, auth_user_id=None, image=None, header_image=None):
    if auth_user_id is None:
        auth_user_id = f'1234brand{num}'
    if image is None:
        image = f'{str(uuid.uuid4())}.png'
    return Brand(
        first_name=f"first_name{num}",
        last_name=f"last_name{num}",
        email=f"email{num}",
        auth_user_id=auth_user_id,
        name=f"name{num}",
        description=f"description{num}",
        website=f"website{num}",
        logo=image,
        header_image=header_image,
        instahandle=f"instahandle{num}",
        values=[],
        categories=[]
    )


def product_generator(num, brand, image=None):
    if image is None:
        image = f'{str(uuid.uuid4())}.png'
    product = Product(
        id=str(uuid.uuid4()),
        created=datetime.utcnow(),
        name=f'prod{num}',
        description=f'prod{num} desc',
        requirements=f'tag1,tag2,tag3',
        brand_id=brand.id,
        image=image)
    product.brand = brand
    return product


class MockBase:
    def __init__(self, returns=None):
        if returns is None:
            returns = {}
        self.__called = OrderedDict({})
        self.__called_with = OrderedDict({})
        self.__returns = returns

    def _spy_time(self, name, args):
        if name not in self.__called:
            self.__called[name] = 0
        self.__called[name] += 1
        self.__called_with[name] = args
        if name not in self.__returns:
            return None
        if isinstance(self.__returns[name], Exception):
            raise self.__returns[name]
        else:
            return self.__returns[name]

    def received_with_args(self, method, args):
        return self.__called_with[method] == args

    def received(self, method, number_of_times):
        if method not in self.__called:
            self.__called[method] = 0
        return self.__called[method] == number_of_times

    def did_not_receive(self, method):
        return method not in self.__called


class InMemorySqliteDataManager(MockBase):

    def __init__(self):
        super().__init__(None)
        self.__engine = create_engine('sqlite:///:memory:')
        session = sessionmaker(bind=self.__engine)
        self.__session = session()
        self.__real_rollback = self.__session.rollback
        self.__real_commit = self.__session.commit
        self.__real_add = self.__session.add
        self.__real_delete = self.__session.delete
        self.__session.rollback = self.__rollback
        self.__session.commit = self.__commit
        self.__session.add = self.__add
        self.__session.delete = self.__delete
        self.__added_entities = []
        self.__deleted_entities = []
        Base.metadata.create_all(self.__engine)

    def __rollback(self):
        self._spy_time('rollback', [])
        self.__real_rollback()

    def __commit(self):
        self._spy_time('commit', [])
        self.__real_commit()

    def __add(self, entity):
        self.__added_entities.append(entity)
        self.__real_add(entity)

    def __delete(self, entity):
        self.__deleted_entities.append(entity)
        self.__real_delete(entity)

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session

    def create_fake_data(self, objects):
        self.__session.bulk_save_objects(objects=objects)

    def changes_were_committed_once(self):
        return self.received('commit', 1) and self.did_not_receive('rollback')

    def changes_were_rolled_back_once(self):
        return self.did_not_receive('commit') and self.received('rollback', 1)

    def no_changes_were_rolled_back_or_committed(self):
        return self.did_not_receive('commit') and self.did_not_receive('rollback')

    def get_last_uncommitted_or_committed_added_entity(self):
        return self.__added_entities.pop()

    def get_last_uncommitted_or_committed_deleted_entity(self):
        return self.__deleted_entities.pop()


class StubDataManager:
    @property
    def engine(self):
        return Mock()

    @property
    def session(self):
        return Mock()


class StubImageRepo:
    def retrieve(self, path):
        return ""

    def delete(self, path):
        pass

    def upload(self, path, image_base64_encoded):
        return ""


class MockImageRepo(MockBase):
    def retrieve(self, path):
        return self._spy_time("retrieve", [path])

    def delete(self, path):
        return self._spy_time("delete", [path])

    def upload(self, path, image_base64_encoded):
        return self._spy_time("upload", [path, image_base64_encoded])

    def upload_was_called_once_with(self, args):
        return self.received('upload', 1) and self.received_with_args('upload', args)

    def delete_was_called_once_with(self, args):
        return self.received('delete', 1) and self.received_with_args('delete', args)

    def upload_was_not_called(self):
        return self.did_not_receive('upload')

    def delete_was_not_called(self):
        return self.did_not_receive('delete')
