from sqlalchemy.orm import Query

from src.common.object_result import ObjectResult
from src.common.result import Result
from src.interfaces.contract.product_repository_interface import ProductRepositoryInterface
from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.entities.product_entity import ProductEntity
from src.domain.models.product_model import ProductModel


class AlchemyProductRepository(ProductRepositoryInterface):

    __data_manager: DataManager

    def __init__(self, data_manager: DataManager):
        self.__data_manager = data_manager

    def feed(self) -> list[ProductModel]:
        pass

