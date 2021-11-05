from sqlalchemy.orm import Query

from src.common.object_result import ObjectResult
from src.common.result import Result
from src.interfaces.contract.product_repository_interface import ProductRepositoryInterface
from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.entities.product_entity import ProductEntity
from src.domain.models.product_model import ProductModel, Owner
import src.data_access_layer.repositories.alchemy_brand_repository as brand_repo


class AlchemyProductRepository(ProductRepositoryInterface):

    __data_manager: DataManager

    def __init__(self, data_manager: DataManager):
        self.__data_manager = data_manager

    def feed(self) -> list[ProductModel]:
        brands: list[brand_repo.BrandEntity] = self.__data_manager.session.query(brand_repo.BrandEntity.id).limit(20).all()
        products = []
        for brand in brands:
            products.extend(self.__data_manager.session
                            .query(ProductEntity)
                            .filter(ProductEntity.brand_id == brand.id)
                            .limit(3)
                            .all())
        limitedProducts = products[:20]
        iterable = map(self.map_out, limitedProducts)
        return list(iterable)

    @staticmethod
    def map_out(product: ProductEntity) -> ProductModel:
        return ProductModel(id=product.id,
                            created=product.created,
                            name=product.name,
                            description=product.description,
                            requirements=product.requirements,
                            brand=Owner(id=product.owner.id,
                                        name=product.owner.name,
                                        created=product.owner.created))
