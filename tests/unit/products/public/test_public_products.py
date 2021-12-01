import pytest

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.web.http_util import PinfluencerResponse
from src.web.processors.products import ProcessPublicProducts
from tests.unit import FakeDataManager, brand_generator, product_generator


@pytest.fixture()
def get_public_products_fixture():
    data_manager = FakeDataManager()
    product_processor = ProcessPublicProducts(data_manager=data_manager)
    return product_processor, data_manager


class TestPublicBrands:
    __result: PinfluencerResponse
    __brands: list[Brand]
    __products: list[Product]
    __product_processor: ProcessPublicProducts
    __data_manager: FakeDataManager

    def __setup(self, get_public_products_fixture, callback=lambda *args: None):
        (self.__product_processor, self.__data_manager) = get_public_products_fixture
        callback()
        self.__result = self.__product_processor.do_process({})

    def __setup_test_data(self):
        self.__brands = [
            brand_generator(1),
            brand_generator(2)
        ]
        self.__products = [
            product_generator(1, self.__brands[0].id),
            product_generator(2, self.__brands[0].id),
            product_generator(3, self.__brands[0].id),
            product_generator(4, self.__brands[0].id),
            product_generator(5, self.__brands[1].id)
        ]
        self.__data_manager.create_fake_data(self.__brands)
        self.__data_manager.create_fake_data(self.__products)
        for product in self.__products:
            def get_brand_product(brand: Brand) -> bool:
                return brand.id == product.brand_id

            product.brand = Brand(id=product.brand_id, name=list(filter(get_brand_product, self.__brands))[0].name)

    def off_test_5_products_are_found_when_db_is_populated(self, get_public_products_fixture):
        self.__setup(get_public_products_fixture, self.__setup_test_data)
        assert self.__result.is_ok()
        length = 5
        assert len(self.__result.body) == length
        for i in range(length):
            assert self.__products[i].as_dict() == self.__result.body[i]

    def off_test_0_products_are_found_when_db_is_empty(self, get_public_products_fixture):
        self.__setup(get_public_products_fixture)
        assert self.__result.is_ok()
        assert len(self.__result.body) == 0
