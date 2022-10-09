import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src._types import Logger

Base = declarative_base()


class SqlAlchemyDataManager:
    def __init__(self, logger: Logger):
        logger.log_debug("new data manager constructed")
        engine_str = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_URL']}/{os.environ['DB_NAME']}"
        engine = create_engine(engine_str)
        self.__engine = engine
        session = sessionmaker(bind=self.__engine,)
        self.__session = session()

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session
