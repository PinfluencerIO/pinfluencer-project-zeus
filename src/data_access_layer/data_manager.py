import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.interfaces.data_manager_interface import DataManagerInterface
from src.web.request_status_manager import RequestStatusManager


class DataManager(DataManagerInterface):
    __session: Session
    __engine: Engine

    def __init__(self, status_manager: RequestStatusManager):
        print("new data manager constructed")
        # engine = create_engine(
        #     'postgresql+auroradataapi://:@/pinfluencerdb',
        #     connect_args={
        #         'aurora_cluster_arn': os.environ['DB_CLUSTER_ARN'],
        #         'secret_arn': os.environ['DB_SECRET_ARN']
        #     }
        # )
        THE_PASSWORD = os.environ['db_password']
        engine = create_engine(
            "postgresql://postgres:%s@pinfluencer.czqff0jhbhz3.eu-west-2.rds.amazonaws.com/pinfluencer" % THE_PASSWORD)
        self.__engine = engine
        session = sessionmaker(bind=self.__engine, autocommit=False)
        self.__session = session()
        self.__status_manager = status_manager

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def session(self) -> Session:
        return self.__session

    def cleanup(self) -> None:
        if self.__status_manager.status:
            self.session.commit()
            print("transaction committed")
        else:
            self.session.rollback()
            print("transaction rollback")
        self.session.close()
        print("session closed")
