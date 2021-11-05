from abc import ABC, abstractmethod

from src.domain.models import ProductModel


class BrandRepositoryInterface(ABC):
    pass


class ProductRepositoryInterface(ABC):

    @abstractmethod
    def feed(self) -> list[ProductModel]:
        pass
