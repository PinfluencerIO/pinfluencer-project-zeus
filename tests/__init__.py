import uuid
from collections import OrderedDict
from datetime import datetime
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data_access_layer import Base
from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product


def brand_generator(num, auth_user_id=None, image=None):
    if auth_user_id is None:
        auth_user_id = f'1234brand{num}'
    if image is None:
        image = f'{str(uuid.uuid4())}.png'
    return Brand(
        id=str(uuid.uuid4()),
        created=datetime.utcnow(),
        name=f'brand{num}',
        description=f'brand{num} desc',
        website=f'test{num}.com',
        email=f'brand{num}@email.com',
        instahandle=f'brand{num}handle',
        image=image,
        auth_user_id=auth_user_id)


def product_generator(num, brand):
    product = Product(
        id=str(uuid.uuid4()),
        created=datetime.utcnow(),
        name=f'prod{num}',
        description=f'prod{num} desc',
        requirements=f'tag1,tag2,tag3',
        brand_id=brand.id,
        image=f'{str(uuid.uuid4())}.png')
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
        self.__session.commit = lambda: self._spy_time('commit', [])
        Base.metadata.create_all(self.__engine)

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session

    def create_fake_data(self, objects):
        self.__session.bulk_save_objects(objects=objects)


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
        assert self.received('upload', 1)
        assert self.received_with_args('upload', args)

    def delete_was_called_once_with(self, args):
        assert self.received('delete', 1)
        assert self.received_with_args('delete', args)

    def upload_was_not_called(self):
        assert self.did_not_receive('upload')

    def delete_was_not_called(self):
        assert self.did_not_receive('delete')
