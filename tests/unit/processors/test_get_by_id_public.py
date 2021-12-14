import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.processors.get_by_id import ProcessGetBy
from tests.unit import StubDataManager

brand = Brand()
brand.id = str(uuid.uuid4())
product = Product()
product.id = str(uuid.uuid4())
product.brand = brand
product.brand_id = brand.id


def mock_db_load_for_brand(id_, r, data_manager):
    if id_ == brand.id:
        return brand
    else:
        return None


def mock_db_load_for_product(id_, r, data_manager):
    if id_ == product.id:
        return product
    else:
        return None


def test_process_public_get_by_id_for_brand():
    processor = ProcessGetBy(mock_db_load_for_brand, 'brand', StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': brand.id}})
    assert pinfluencer_response.is_ok() is True
    assert pinfluencer_response.body == brand.as_dict()


def test_process_public_get_by_id_for_product():
    processor = ProcessGetBy(mock_db_load_for_product, 'product', StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'product_id': product.id}})
    assert pinfluencer_response.is_ok() is True
    assert pinfluencer_response.body == product.as_dict()


def test_process_public_get_by_id_for_brand_not_found():
    processor = ProcessGetBy(mock_db_load_for_brand, 'brand', StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 404


def test_process_public_get_by_id_for_brand_invalid_uuid():
    processor = ProcessGetBy(mock_db_load_for_brand, 'brand', StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': '213-123'}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400
