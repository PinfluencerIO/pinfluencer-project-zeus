from src.common.object_result import ObjectResult
from src.common.result import Result
from src.interfaces.contract.brand_repository_interface import BrandRepositoryInterface
from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.entities.brand_entity import BrandEntity
from src.domain.models.brand_model import BrandModel


class AlchemyBrandRepository(BrandRepositoryInterface):

    __data_manager: DataManager

    def __init__(self, data_manager: DataManager):
        self.__data_manager = data_manager
