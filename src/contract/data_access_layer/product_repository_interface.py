from abc import ABC

from src.contract.data_access_layer.createable_interface import CreateableInterface
from src.contract import ReadableInterface
from src.data_access_layer.entities.product_entity import Product


class ProductRepositoryInterface(CreateableInterface[Product], ReadableInterface[Product], metaclass=ABC):
    def create(self, data: Product) -> bool:
        pass

    def read(self, id: str) -> Product:
        pass