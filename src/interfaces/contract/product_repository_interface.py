from abc import ABC, abstractmethod

from src.common.object_result import ObjectResult
from src.common.result import Result
from src.domain.models.product_model import ProductModel


class ProductRepositoryInterface(ABC):

    @abstractmethod
    def feed(self) -> list[ProductModel]:
        pass

