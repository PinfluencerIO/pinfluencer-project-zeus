import os

from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.image_repository import S3ImageRepository

from src.interfaces.data_manager_interface import DataManagerInterface
from src.interfaces.image_repository_interface import ImageRepositoryInterface
from tests.unit import FakeDataManager


class Container:
    data_manager: DataManagerInterface
    image_repository: ImageRepositoryInterface

    def __init__(self):
        print("new container constructed")
        if 'IN_MEMORY' in os.environ:
            self.data_manager = FakeDataManager()
        else:
            self.data_manager = DataManager()
        self.image_repository = S3ImageRepository()
