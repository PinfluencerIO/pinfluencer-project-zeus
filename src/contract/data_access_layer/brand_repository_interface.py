from abc import ABC, abstractmethod

from src.common.object_result import ObjectResult
from src.common.result import Result
from src.contract.data_access_layer.createable_interface import CreatableInterface
from src.contract.data_access_layer.deleteable_interface import DeletableInterface
from src.contract.data_access_layer.readable_interface import ReadableInterface
from src.contract.data_access_layer.updatable_interface import UpdatableInterface
from src.domain.models.brand_model import BrandModel


class BrandRepositoryInterface(CreatableInterface[BrandModel],
                               ReadableInterface[BrandModel],
                               UpdatableInterface[BrandModel],
                               DeletableInterface[BrandModel],
                               metaclass=ABC):

    @abstractmethod
    def create(self, data: BrandModel) -> ObjectResult[str]:
        pass

    @abstractmethod
    def read(self, id: str) -> BrandModel:
        pass

    @abstractmethod
    def readall(self) -> list[BrandModel]:
        pass

    @abstractmethod
    def update(self, data: BrandModel) -> Result:
        pass

    @abstractmethod
    def delete(self, id: str) -> Result:
        pass
