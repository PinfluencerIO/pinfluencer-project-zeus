from abc import ABC

from src.contract.data_access_layer.createable_interface import CreateableInterface
from src.contract import ReadableInterface
from src.data_access_layer.entities.product_entity import ProductEntity


class ProductRepositoryInterface(CreateableInterface[ProductEntity], ReadableInterface[ProductEntity], metaclass=ABC):
    def create(self, data: ProductEntity) -> bool:
        pass

    def read(self, id: str) -> ProductEntity:
        pass