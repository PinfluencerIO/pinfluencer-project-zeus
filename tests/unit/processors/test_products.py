import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.filters import FilterResponse
from src.filters.valid_id_filters import LoadResourceById
from src.processors.products import ProcessPublicProducts, ProcessPublicGetProductBy
from tests.unit import StubDataManager


def test_load_all_products_response_200():
    processor = ProcessPublicProducts(StubDataManager())
    processor.load_all_products = mock_response_from_db

    pinfluencer_response = processor.do_process({})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) is list


# @patch('src.filters.valid_id_filters.load_by_id')
def test_process_successful_public_get_product_by_id():
    load_resource = LoadResourceById(StubDataManager(), 'product')
    uuid_ = uuid.uuid4()
    processor = ProcessPublicGetProductBy(load_resource, StubDataManager())
    processor.load_product_from_cmd = mock_load_product
    pinfluencer_response = processor.do_process(
        {'pathParameters': {'product_id': str(uuid_)}})
    assert pinfluencer_response.is_ok() is True


def test_process_unsuccessful_public_get_brand_by_id():
    load_resource = LoadResourceById(StubDataManager(), 'product')
    uuid_ = uuid.uuid4()
    processor = ProcessPublicGetProductBy(load_resource, StubDataManager())
    processor.load_product_from_cmd = mock_load_product_failed
    pinfluencer_response = processor.do_process(
        {'pathParameters': {'product_id': str(uuid_)}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def mock_load_product(event):
    return FilterResponse('', 200, mock_response_from_db()[0])


def mock_load_product_failed(event):
    return FilterResponse('', 400, {})


def mock_response_from_db():
    brand = Brand()
    product1 = Product()
    product1.brand = brand
    product2 = Product()
    product2.brand = brand
    return [product1, product2]
