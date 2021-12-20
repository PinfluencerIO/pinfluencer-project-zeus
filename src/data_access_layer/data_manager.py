import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class DataManager:
    __session: Session
    __engine: Engine

    def __init__(self):
        print("new data manager constructed")
        engine = create_engine(
            f"mysql+mysqlconnector://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
            f"@{os.environ['DB_URL']}/{os.environ['DB_NAME']}")
        self.__engine = engine
        session = sessionmaker(bind=self.__engine, autocommit=False)
        self.__session = session()

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def session(self) -> Session:
        return self.__session
