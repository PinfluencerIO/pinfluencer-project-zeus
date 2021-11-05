from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.repositories import AlchemyProductRepository
from src.interfaces.contract.repositories import ProductRepositoryInterface


class Container:
    data_manager: DataManager
    product_repo: ProductRepositoryInterface

    def __init__(self):
        self.data_manager = DataManager()
        self.product_repo = AlchemyProductRepository(data_manager=self.data_manager)