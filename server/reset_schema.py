import os

from src.app import logger_factory
from src.data import SqlAlchemyDataManager, Base

# for logging and other DI switching
os.environ["ENVIRONMENT"] = "TEST"

data_manager = SqlAlchemyDataManager(logger=logger_factory())
Base.metadata.create_all(bind=data_manager.engine)
