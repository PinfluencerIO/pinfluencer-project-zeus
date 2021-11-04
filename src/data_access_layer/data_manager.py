from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
import os


class DataManager:
    __session: Session
    __engine: Engine

    def __init__(self):
        engine = create_engine(
            'postgresql+pydataapi://',
            connect_args={
                'resource_arn': os.environ['DB_CLUSTER_ARN'],
                'secret_arn': os.environ['DB_SECRET_ARN'],
                'database': os.environ['DATABASE_NAME']
            }
        )
        self.__engine = engine
        session = sessionmaker(bind=self.__engine)
        self.__session = session()

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def session(self) -> Session:
        return self.__session
