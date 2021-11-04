from src.common.object_result import ObjectResult
from src.common.result import Result
from src.interfaces.contract.brand_repository_interface import BrandRepositoryInterface
from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.entities.brand_entity import BrandEntity
from src.domain.models.brand_model import BrandModel
import src.data_access_layer.repositories.alchemy_product_repository as product_repo


class AlchemyBrandRepository(BrandRepositoryInterface):
    __data_manager: DataManager

    def __init__(self, data_manager: DataManager):
        self.__data_manager = data_manager

    @staticmethod
    def map_out(brand: BrandEntity, show_products: bool) -> BrandModel:
        brand = BrandModel(id=brand.id,
                           created=brand.created,
                           name=brand.name,
                           description=brand.description,
                           website=brand.website,
                           email=brand.email,
                           auth_user_id=brand.auth_user_id,
                           products=[])
        if show_products:
            brand.products = list(map(product_repo.AlchemyProductRepository.map_out, brand.products))
        return brand
