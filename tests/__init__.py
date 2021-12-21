import uuid
from collections import OrderedDict
from datetime import datetime
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data_access_layer import Base
from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product


def brand_generator(num):
    return Brand(
        id=str(uuid.uuid4()),
        created=datetime.utcnow(),
        name=f'brand{num}',
        description=f'brand{num} desc',
        website=f'test{num}.com',
        email=f'brand{num}@email.com',
        instahandle=f'brand{num}handle',
        image=f'{str(uuid.uuid4())}.png',
        auth_user_id=f'1234brand{num}')


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


class InMemorySqliteDataManager:

    def __init__(self):
        self.__engine = create_engine('sqlite:///:memory:')
        session = sessionmaker(bind=self.__engine)
        self.__session = session()
        Base.metadata.create_all(self.__engine)

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session

    def create_fake_data(self, objects):
        self.__session.bulk_save_objects(objects=objects)
        self.__session.commit()


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


class MockBase:
    def __init__(self, returns):
        self.__called = OrderedDict({})
        self.__called_with = OrderedDict({})
        self.__returns = returns

    def _spy_time(self, name, args):
        if name not in self.__called:
            self.__called[name] = 0
        self.__called[name] += 1
        self.__called_with[name] = args
        if name not in self.__returns:
            pass
        if isinstance(self.__returns[name], Exception):
            raise self.__returns[name]
        else:
            return self.__returns[name]

    def received_with_args(self, method, args):
        return self.__called_with[method] == args

    def received(self, method, number_of_times):
        return self.__called[method] == number_of_times


class MockImageRepo(MockBase):
    def retrieve(self, path):
        return self._spy_time("delete", [path])

    def delete(self, path):
        return self._spy_time("delete", [path])

    def upload(self, path, image_base64_encoded):
        return self._spy_time("upload", [path, image_base64_encoded])
