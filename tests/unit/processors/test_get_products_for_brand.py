import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.processors.get_products_for_brand import ProcessGetProductsForBrand
from tests import StubDataManager

b = Brand()
b.id = str(uuid.uuid4())
p = Product()
p.id = str(uuid.uuid4())
p.brand = b
p.brand_id = b.id


def mock_db_load(id_, data_manager):
    if id_ == b.id:
        return [p]
    else:
        return []


def test_process_public_all_products_for_brand():
    processor = ProcessGetProductsForBrand(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': b.id}})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) == list


def test_process_public_all_products_for_brand_failed_to_load_by_id():
    processor = ProcessGetProductsForBrand(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 404


def test_process_public_all_products_for_brand_failed_invalid_uuid():
    processor = ProcessGetProductsForBrand(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': '123-123'}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400
