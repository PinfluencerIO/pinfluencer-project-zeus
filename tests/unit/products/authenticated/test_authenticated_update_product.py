import json

import pytest

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.filters import *
from src.filters.authorised_filter import AuthFilter, OwnerOnly
from src.filters.payload_validation import ProductPutPayloadValidation
from src.filters.valid_id_filters import LoadResourceById
from src.pinfluencer_response import PinfluencerResponse
from src.web.processors.products import ProcessPublicProducts, ProcessAuthenticatedPutProduct
from src.web.request_status_manager import RequestStatusManager
from tests.unit import FakeDataManager, brand_generator, product_generator


@pytest.fixture()
def update_auth_product_fixture():
    data_manager = FakeDataManager()
    auth_filter = AuthFilter(data_manager)
    valid_product_filter = LoadResourceById('product')
    status_manager = RequestStatusManager()
    product_processor = ProcessAuthenticatedPutProduct(
        FilterChainImp(
            [auth_filter, valid_product_filter, OwnerOnly('product'),
             ProductPutPayloadValidation()]), data_manager, status_manager)
    return product_processor, data_manager


class TestPublicBrands:
    __result: PinfluencerResponse
    __brands: list[Brand]
    __products: list[Product]
    __product_processor: ProcessPublicProducts
    __data_manager: FakeDataManager
    __event: dict
    __product_new: dict

    def __setup(self, update_auth_product_fixture, callback=lambda *args: None):
        (self.__product_processor, self.__data_manager) = update_auth_product_fixture
        callback()
        self.__product_processor.run_filters(event=self.__event)
        self.__result = self.__product_processor.do_process(self.__event)

    def __setup_test_data(self):
        self.__brands = [
            brand_generator(1)
        ]
        self.__products = [
            product_generator(1, self.__brands[0].id)
        ]
        self.__data_manager.create_fake_data(self.__brands)
        self.__data_manager.create_fake_data(self.__products)
        for product in self.__products:
            def get_brand_product(brand: Brand) -> bool:
                return brand.id == product.brand_id

            product.brand = Brand(id=product.brand_id, name=list(filter(get_brand_product, self.__brands))[0].name)
        self.__product_new = {
            "name": "newprod",
            "description": "newdesc",
            "requirements": "tag1, tag2, tag3"
        }
        self.__event = {
            'pathParameters': {
                'product_id': self.__products[0].id
            },
            'body': json.dumps(self.__product_new),
            'requestContext': {'authorizer': {'jwt': {'claims': {'cognito:username': "1234brand1"}}}}
        }

    def off_test_new_product_changes_take_affect_when_product_is_changed(self, update_auth_product_fixture):
        self.__setup(update_auth_product_fixture, self.__setup_test_data)
        assert self.__result.is_ok()
        product: Product = self.__data_manager.session.query(Product).filter(
            Product.id == self.__products[0].id).first()
        assert product.name == self.__product_new['name']
        assert product.description == self.__product_new['description']
        assert product.requirements == self.__product_new['requirements']
