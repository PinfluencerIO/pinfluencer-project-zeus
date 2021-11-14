from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.data_access_layer import Base
from src.data_access_layer.brand import Brand
from src.interfaces.data_manager_interface import DataManagerInterface


class FakeDataManager(DataManagerInterface):

    def __init__(self):
        self.__engine: Engine = create_engine('sqlite:///:memory:')
        session = sessionmaker(bind=self.__engine)
        self.__session = session()
        Base.metadata.create_all(self.__engine)
        self.create_fake_data()

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def session(self) -> Session:
        return self.__session

    def create_fake_data(self):
        self.__session.bulk_save_objects([
            Brand(name='brand1',
                  description='brand1 desc',
                  website='test.com',
                  email='brand1@email.com',
                  instahandle='brand1handle',
                  image='id.png',
                  auth_user_id='1234brand1'),
            Brand(name='brand2',
                  description='brand2 desc',
                  website='test2.com',
                  email='brand2@email.com',
                  instahandle='brand2handle',
                  image='id2.png',
                  auth_user_id='1234brand2'),
            Brand(name='brand3',
                  description='brand1 desc',
                  website='test3.com',
                  email='brand3@email.com',
                  instahandle='brand3handle',
                  image='id3.png',
                  auth_user_id='1234brand3')
        ])
        self.__session.commit()
