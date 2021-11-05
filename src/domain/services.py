from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.repositories.alchemy_product_repository import AlchemyProductRepository
from src.interfaces.contract.product_repository_interface import ProductRepositoryInterface
from src.web.processors.feed import ProcessPublicFeed


class Container:
    data_manager: DataManager
    product_repo: ProductRepositoryInterface
    process_public_feed: ProcessPublicFeed

    def __init__(self):
        self.data_manager = DataManager()
        self.product_repo = AlchemyProductRepository(data_manager=self.data_manager)