import uuid
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


class FakeImageRepo:
    def retrieve(self, path):
        pass

    def delete(self, path):
        pass

    def upload(self, path, image_base64_encoded):
        pass
