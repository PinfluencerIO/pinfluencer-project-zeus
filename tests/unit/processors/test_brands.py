import uuid
from unittest.mock import patch

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.filters.valid_id_filters import LoadResourceById
from src.processors.brands import ProcessPublicBrands, ProcessPublicGetBrandBy, ProcessPublicAllProductsForBrand
from tests.unit import StubDataManager


@patch('src.processors.brands.to_list')
def test_process_public_brands_response_is_200(mock_to_list):
    mock_to_list.return_value = [{}]
    process_public_brands = ProcessPublicBrands(StubDataManager())
    pinfluencer_response = process_public_brands.do_process({})
    assert pinfluencer_response.is_ok() is True


@patch('src.filters.valid_id_filters.load_by_id')
def test_process_successful_public_get_brand_by_id(mock_load_by_id):
    load_resource = LoadResourceById(StubDataManager(), 'brand')
    uuid_ = uuid.uuid4()
    brand = Brand()
    mock_load_by_id.return_value = brand
    processor = ProcessPublicGetBrandBy(load_resource)
    pinfluencer_response = processor.do_process(
        {'pathParameters': {'brand_id': str(uuid_)}})
    assert pinfluencer_response.is_ok() is True
    assert pinfluencer_response.body == brand.as_dict()


@patch('src.filters.valid_id_filters.load_by_id')
def test_process_unsuccessful_public_get_brand_by_id(mock_load_by_id):
    load_resource = LoadResourceById(StubDataManager(), 'brand')
    mock_load_by_id.return_value = None
    processor = ProcessPublicGetBrandBy(load_resource)
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


@patch('src.processors.brands.load_all_products_for_brand_id')
@patch('src.filters.valid_id_filters.load_by_id')
def test_process_public_all_products_for_brand(mock_load_by_id, mock_load_all_products_for_brand):
    brand = Brand()
    mock_load_by_id.return_value = brand
    product = Product()
    product.brand = brand
    mock_load_all_products_for_brand.return_value = [product]
    load_resource = LoadResourceById(StubDataManager(), 'brand')
    processor = ProcessPublicAllProductsForBrand(load_resource, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is True


@patch('src.processors.brands.load_all_products_for_brand_id')
@patch('src.filters.valid_id_filters.load_by_id')
def test_process_public_all_products_for_brand(mock_load_by_id, mock_load_all_products_for_brand):
    mock_load_by_id.return_value = None
    load_resource = LoadResourceById(StubDataManager(), 'brand')
    processor = ProcessPublicAllProductsForBrand(load_resource, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400
