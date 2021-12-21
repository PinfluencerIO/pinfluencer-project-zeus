import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.processors.get_for_auth_user import ProcessGetForAuthenticatedUser, ProcessGetForAuthenticatedUserAsCollection
from tests import StubDataManager


def test_process_get_for_authenticated_user():
    processor = ProcessGetForAuthenticatedUser(mock_load_for_auth_user, StubDataManager())
    response = processor.do_process({
        'pathParameters': {
            'product_id': str(uuid.uuid4())
        },
        'requestContext': {
            "authorizer": {
                "jwt": {
                    "claims": {
                        "cognito:username": "google_106146319509880568839",
                        "email": "dom@pinfluencer.io",
                    }
                }
            }
        }
    })
    assert response.is_ok() is True
    assert response.status_code == 200
    assert type(response.body) == dict


def test_process_get_for_authenticated_user_fail_db_read():
    processor = ProcessGetForAuthenticatedUser(mock_db_load_failed_to_read, StubDataManager())
    response = processor.do_process({
        'pathParameters': {
            'product_id': str(uuid.uuid4())
        },
        'requestContext': {
            "authorizer": {
                "jwt": {
                    "claims": {
                        "cognito:username": "google_106146319509880568839",
                        "email": "dom@pinfluencer.io",
                    }
                }
            }
        }
    })
    assert response.is_ok() is False
    assert response.status_code == 404


def test_process_get_for_authenticated_user_as_collection():
    processor = ProcessGetForAuthenticatedUserAsCollection(mock_load_collection_for_auth_user, StubDataManager())
    response = processor.do_process({
        'pathParameters': {
            'product_id': str(uuid.uuid4())
        },
        'requestContext': {
            "authorizer": {
                "jwt": {
                    "claims": {
                        "cognito:username": "google_106146319509880568839",
                        "email": "dom@pinfluencer.io",
                    }
                }
            }
        }
    })
    assert response.is_ok() is True
    assert response.status_code == 200
    assert type(response.body) == list


def test_process_get_for_authenticated_user_as_collection_failed_db_read():
    processor = ProcessGetForAuthenticatedUserAsCollection(mock_db_load_failed_to_read, StubDataManager())
    response = processor.do_process({
        'pathParameters': {
            'product_id': str(uuid.uuid4())
        },
        'requestContext': {
            "authorizer": {
                "jwt": {
                    "claims": {
                        "cognito:username": "google_106146319509880568839",
                        "email": "dom@pinfluencer.io",
                    }
                }
            }
        }
    })
    assert response.is_ok() is False
    assert response.status_code == 404


def mock_load_for_auth_user(auth_user_id, data_manager):
    brand = Brand()
    brand.id = str(uuid.uuid4())
    return brand


def mock_load_collection_for_auth_user(auth_user_id, data_manager):
    brand = Brand()
    brand.id = str(uuid.uuid4())
    product = Product()
    product.id = str(uuid.uuid4())
    product.brand = brand
    return [product]


def mock_db_load_failed_to_read(auth_user_id, data_manager):
    return None
