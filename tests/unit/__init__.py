import uuid
from collections import OrderedDict
from datetime import datetime
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.data_access_layer import Base, BaseEntity
from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.interfaces.data_manager_interface import DataManagerInterface
from src.interfaces.image_repository_interface import ImageRepositoryInterface


def brand_generator(num: int) -> Brand:
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


def product_generator(num: int, brand: Brand) -> Product:
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


class InMemorySqliteDataManager(DataManagerInterface):

    def __init__(self):
        self.__engine: Engine = create_engine('sqlite:///:memory:')
        session = sessionmaker(bind=self.__engine)
        self.__session = session()
        Base.metadata.create_all(self.__engine)

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def session(self) -> Session:
        return self.__session

    def create_fake_data(self, objects: list[BaseEntity]):
        self.__session.bulk_save_objects(objects=objects)
        self.__session.commit()


class StubDataManager(DataManagerInterface):
    @property
    def engine(self) -> Engine:
        return Mock()

    @property
    def session(self) -> Session:
        return Mock()


class StubImageRepo(ImageRepositoryInterface):
    def retrieve(self, path: str) -> str:
        return ""

    def delete(self, path: str) -> None:
        pass

    def upload(self, path: str, image_base64_encoded: str) -> str:
        return ""


class FakeImageRepo(ImageRepositoryInterface):
    def __init__(self):
        self.__images = OrderedDict({
            "": ""
        })

    def retrieve(self, path: str) -> str:
        return self.__images[path]

    def delete(self, path: str) -> None:
        del self.__images[path]

    def upload(self, path: str, image_base64_encoded: str) -> str:
        path = f"{path}/{str(uuid.uuid4())}.png"
        self.__images.update({f"{path}": image_base64_encoded})
        return path
