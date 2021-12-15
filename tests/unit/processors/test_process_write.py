import json
import os
import uuid

from _pytest.fixtures import fixture

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.data_access_layer.write_data_access import NotFoundException
from src.processors.write_for_auth_user import ProcessWriteForAuthenticatedUser, \
    ProcessWriteWithValidationForAuthenticatedUser, ProcessWriteForAuthenticatedUserWithProductId
from tests.unit import StubDataManager

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

my_data_path = os.path.join(THIS_DIR, os.pardir, '../../events/')


@fixture
def new_brand_event():
    with open(my_data_path + 'create_brand.json') as f:
        data = json.load(f)
    return data


@fixture
def update_product_event():
    with open(my_data_path + 'update_product.json') as f:
        data = json.load(f)
    return data


@fixture
def new_brand_event_invalid():
    with open(my_data_path + 'create_brand_invalid.json') as f:
        data = json.load(f)
    return data


def test_do_process_write_new(new_brand_event):
    process = ProcessWriteForAuthenticatedUser('brand', 'post', mock_db_write, StubDataManager())
    pinfluencer_response = process.do_process(new_brand_event)

    assert pinfluencer_response.is_ok() is True
    assert pinfluencer_response.status_code == 201


def test_do_process_write_update(new_brand_event):
    process = ProcessWriteForAuthenticatedUser('brand', 'put', mock_db_write, StubDataManager())
    pinfluencer_response = process.do_process(new_brand_event)

    assert pinfluencer_response.is_ok() is True
    assert pinfluencer_response.status_code == 200


def test_do_process_write_failed_validation(new_brand_event_invalid):
    process = ProcessWriteWithValidationForAuthenticatedUser('brand', 'post', mock_db_write, StubDataManager())
    pinfluencer_response = process.do_process(new_brand_event_invalid)

    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_do_process_write_failed_db_update(new_brand_event):
    process = ProcessWriteForAuthenticatedUser('brand', 'post', mock_db_write_none, StubDataManager())
    pinfluencer_response = process.do_process(new_brand_event)

    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 404


def test_process_write_for_authenticated_user_with_product_id(update_product_event):
    process = ProcessWriteForAuthenticatedUserWithProductId('product', 'put', mock_db_update_product, StubDataManager())
    pinfluencer_response = process.do_process(update_product_event)

    assert pinfluencer_response.is_ok() is True
    assert pinfluencer_response.status_code == 200


def mock_db_write(auth_user_id, dict_, data_manager):
    return Brand()


def mock_db_update_product(auth_user_id, dict_, data_manager):
    product = Product()
    product.id = str(uuid.uuid4())
    brand = Brand()
    brand.id = str(uuid.uuid4())
    product.brand = brand
    return product


def mock_db_write_none(auth_user_id, dict_, data_manager):
    raise NotFoundException('')
