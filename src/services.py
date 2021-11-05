from src.data_access_layer.data_manager import DataManager
from src.interfaces.data_manager_interface import DataManagerInterface
from src.web.filters import AuthFilter


class Container:
    data_manager: DataManagerInterface
    auth_filter: AuthFilter

    def __init__(self):
        self.data_manager = DataManager()
        self.auth_filter = AuthFilter(self.data_manager)
