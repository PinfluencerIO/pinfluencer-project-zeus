import uuid
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data.entities import BrandEntity, Base
from src.domain.models import Brand


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


class StubDataManager:
    @property
    def engine(self):
        return Mock()

    @property
    def session(self):
        return Mock()


class StubImageRepo:
    def retrieve(path):
        return ""

    def delete(self, path):
        pass

    def upload(self, path, image_base64_encoded):
        return ""
