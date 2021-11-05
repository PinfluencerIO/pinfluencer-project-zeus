from src.data_access_layer.data_manager import DataManager
from src.data_access_layer.entites import BrandEntity, ProductEntity
from src.domain.models import ProductModel, Owner, BrandModel
from src.interfaces.contract.repositories import BrandRepositoryInterface, ProductRepositoryInterface


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
            brand.products = list(map(AlchemyProductRepository.map_out, brand.products))
        return brand


class AlchemyProductRepository(ProductRepositoryInterface):

    __data_manager: DataManager

    def __init__(self, data_manager: DataManager):
        self.__data_manager = data_manager

    def feed(self) -> list[ProductModel]:
        brands: list[BrandEntity] = self.__data_manager.session.query(BrandEntity.id).limit(20).all()
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
