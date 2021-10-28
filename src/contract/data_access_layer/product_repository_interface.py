from abc import ABC

from src.contract.data_access_layer.createable_interface import CreatableInterface
from src.contract.data_access_layer.deleteable_interface import DeletableInterface
from src.contract.data_access_layer.readable_interface import ReadableInterface, T
from src.contract.data_access_layer.updatable_interface import UpdatableInterface
from src.domain.models.product_model import ProductModel


class ProductRepositoryInterface(CreatableInterface[ProductModel],
                                 ReadableInterface[ProductModel],
                                 UpdatableInterface[ProductModel],
                                 DeletableInterface[ProductModel],
                                 metaclass=ABC):
    def create(self, data: ProductModel) -> bool:
        pass

    def read(self, id: str) -> ProductModel:
        pass

    def readall(self, id: str) -> ProductModel:
        pass

    def update(self, data: T) -> bool:
        pass

    def delete(self, data: T) -> bool:
        pass
