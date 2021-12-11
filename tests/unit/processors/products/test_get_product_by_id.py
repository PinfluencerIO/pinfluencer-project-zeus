import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.filters import FilterResponse
from src.processors.products.get_product_by_id import ProcessPublicGetProductBy
from tests.unit import StubDataManager
from tests.unit.processors.brands import MockFilterResponse
from tests.unit.processors.products.test_products import mock_load_product


def test_get_product_by_id():
    brand = Brand()
    brand.id = str(uuid.uuid4())
    product = Product()
    uuid_ = uuid.uuid4()
    product.id = uuid_
    product.brand = brand
    load_resource = MockFilterResponse(FilterResponse('', 200, product.as_dict()))
    processor = ProcessPublicGetProductBy(load_resource, StubDataManager())
    processor.load_product_from_cmd = mock_load_product
    pinfluencer_response = processor.do_process(
        {'pathParameters': {'product_id': str(uuid_)}})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) == dict
    assert pinfluencer_response.body['id'] == uuid_


def test_get_product_by_id_failed_to_find_product():
    uuid_ = uuid.uuid4()

    load_resource = MockFilterResponse(FilterResponse('', 404, {}))
    processor = ProcessPublicGetProductBy(load_resource, StubDataManager())
    processor.load_product_from_cmd = mock_load_product
    pinfluencer_response = processor.do_process(
        {'pathParameters': {'product_id': str(uuid_)}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 404


def test_get_product_by_id_failed_to_process_event():
    uuid_ = uuid.uuid4()

    load_resource = MockFilterResponse(FilterResponse('', 400, {}))
    processor = ProcessPublicGetProductBy(load_resource, StubDataManager())
    processor.load_product_from_cmd = mock_load_product
    pinfluencer_response = processor.do_process(
        {'pathParameters': {'product_id': str(uuid_)}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400
