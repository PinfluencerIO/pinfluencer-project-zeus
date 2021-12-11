import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.filters import FilterResponse
from src.processors.brands.get_products_for_brand import ProcessPublicAllProductsForBrand
from tests.unit import StubDataManager
from tests.unit.processors.brands import mock_load_all_products_for_brand_id, MockFilterResponse

b = Brand()
b.id = str(uuid.uuid4())
p = Product()
p.id = str(uuid.uuid4())
p.brand = b
p.brand_id = b.id


def mock_db_load(id, data_manager):
    if id == b.id:
        return [p]
    else:
        return []


def test_process_public_all_products_for_brand():
    processor = ProcessPublicAllProductsForBrand(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': b.id}})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) == list


def test_process_public_all_products_for_brand_failed_to_load_by_id():
    processor = ProcessPublicAllProductsForBrand(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 404


def test_process_public_all_products_for_brand_failed_invalid_uuid():
    processor = ProcessPublicAllProductsForBrand(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': '123-123'}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400
