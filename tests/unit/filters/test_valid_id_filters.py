import uuid
from unittest.mock import patch

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.filters.valid_id_filters import LoadResourceById
from tests.unit import StubDataManager


@patch('src.filters.valid_id_filters.load_by_id')
def test_load_resources_id_succeeds_for_known_brand_resource_id(mock_load):
    mock_load.return_value = Brand()

    manager = StubDataManager()
    _filter = LoadResourceById(manager, 'brand')

    uuid_ = uuid.uuid4()
    response = _filter.do_filter({'pathParameters': {'brand_id': str(uuid_)}})

    assert response.is_success() is True
    assert response.get_code() == 200
    mock_load.assert_called_with(str(uuid_), Brand, manager)


@patch('src.filters.valid_id_filters.load_by_id')
def test_load_resources_id_succeeds_for_known_product_resource_id(mock_load):
    product = Product()
    product.brand = Brand()
    mock_load.return_value = product

    manager = StubDataManager()
    _filter = LoadResourceById(manager, 'product')

    uuid_ = uuid.uuid4()
    response = _filter.do_filter({'pathParameters': {'product_id': str(uuid_)}})

    assert response.is_success() is True
    assert response.get_code() == 200
    mock_load.assert_called_with(str(uuid_), Product, manager)


@patch('src.filters.valid_id_filters.load_by_id')
def test_load_resources_id_fails_for_unknown_resource_id(mock_load):
    mock_load.return_value = None

    _filter = LoadResourceById(StubDataManager(), 'brand')

    response = _filter.do_filter({'pathParameters': {'brand_id': str(uuid.uuid4())}})

    assert response.is_success() is False
    assert response.get_code() == 404


def test_load_resources_id_fails_when_event_missing_key():
    _filter = LoadResourceById(StubDataManager(), 'brand')
    response = _filter.do_filter({'pathParameters': {}})
    assert response.is_success() is False
    assert response.get_code() == 400


def test_load_resources_id_fails_when_event_root_missing_key():
    _filter = LoadResourceById(StubDataManager(), 'brand')
    response = _filter.do_filter({'sadf': {}})
    assert response.is_success() is False
    assert response.get_code() == 400


def test_load_resources_id_fails_when_event_contains_invalid_uuid():
    _filter = LoadResourceById(StubDataManager(), 'brand')
    response = _filter.do_filter({'pathParameters': {'brand_id': '123-123-123-123-123'}})
    assert response.is_success() is False
    assert response.get_code() == 400
