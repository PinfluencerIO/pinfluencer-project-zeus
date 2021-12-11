import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.processors.products.get_product_by_id import ProcessPublicGetProductBy
from tests.unit import StubDataManager

b = Brand()
b.id = str(uuid.uuid4())
p = Product()
p.id = str(uuid.uuid4())
p.brand = b
p.brand_id = b.id


def mock_db_load(id, r, data_manager):
    if id == p.id:
        return p
    else:
        return None


def test_get_product_by_id():
    processor = ProcessPublicGetProductBy(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'product_id': p.id}})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) == dict
    assert pinfluencer_response.body['id'] == p.id


def test_get_product_by_id_failed_to_find_product():
    processor = ProcessPublicGetProductBy(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'product_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 404


def test_get_product_by_id_failed_invalid_uuid():
    processor = ProcessPublicGetProductBy(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'product_id': '123-123'}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400
