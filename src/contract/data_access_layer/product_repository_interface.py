from abc import ABC, abstractmethod

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

    @abstractmethod
    def create(self, data: ProductModel) -> bool:
        pass

    @abstractmethod
    def read(self, id: str) -> ProductModel:
        pass

    @abstractmethod
    def readall(self, id: str) -> ProductModel:
        pass

    @abstractmethod
    def update(self, data: T) -> bool:
        pass

    @abstractmethod
    def delete(self, data: T) -> bool:
        pass
