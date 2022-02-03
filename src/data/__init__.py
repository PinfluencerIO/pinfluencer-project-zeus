import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class SqlAlchemyDataManager:
    def __init__(self):
        print("new data manager constructed")
        engine = create_engine(
            f"mysql+mysqlconnector://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
            f"@{os.environ['DB_URL']}/{os.environ['DB_NAME']}")
        self.__engine = engine
        session = sessionmaker(bind=self.__engine, autocommit=False)
        self.__session = session()

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session


class DataManageFactory:
    @staticmethod
    def build():
        if 'IN_MEMORY' in os.environ:
            from tests import InMemorySqliteDataManager
            print('Creating an in memory mysql database')
            return InMemorySqliteDataManager()
        else:
            return SqlAlchemyDataManager()


DEFAULT_BRAND_LOGO = "default_brand_logo.png"
DEFAULT_BRAND_HEADER_IMAGE = "default_brand_header_image.png"
DEFAULT_INFLUENCER_PROFILE_IMAGE = "default_influencer_profile_image.png"


