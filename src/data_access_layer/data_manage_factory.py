import os

from src.data_access_layer.data_manager import DataManager


class DataManageFactory:
    @staticmethod
    def build():
        if 'IN_MEMORY' in os.environ:
            from tests import InMemorySqliteDataManager
            print('Creating an in memory mysql database')
            return InMemorySqliteDataManager()
        else:
            return DataManager()
