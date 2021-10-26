from sqlalchemy.ext.declarative import declarative_base

from functions.data_access_layer.data_manager import DataManager

DBManager = DataManager()
Base = declarative_base()


def initialize():
    Base.metadata.create_all(bind=DBManager.engine)
