import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.processors.products import ProcessPublicProducts
from tests.unit import StubDataManager


def test_load_all_products_response_200():
    processor = ProcessPublicProducts(StubDataManager())
    processor.load_all_products = mock_response_from_db

    pinfluencer_response = processor.do_process({})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) is list


def mock_response_from_db():
    brand = Brand()
    product1 = Product()
    product1.brand = brand
    product2 = Product()
    product2.brand = brand
    return [product1, product2]
