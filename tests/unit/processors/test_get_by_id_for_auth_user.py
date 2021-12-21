import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.processors.get_by_id_for_auth_user import ProcessGetByForAuthenticatedUser
from tests import StubDataManager


def test_do_process_get_by_id_for_authenticated_user():
    processor = ProcessGetByForAuthenticatedUser(mock_db_read, 'product', StubDataManager())
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


def test_do_process_get_by_id_for_authenticated_user_failed_product_id_validation():
    processor = ProcessGetByForAuthenticatedUser(mock_db_read, 'product', StubDataManager())
    response = processor.do_process({
        'pathParameters': {
            'product_id': '123-123'
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
    assert response.status_code == 400


def test_do_process_get_by_id_for_authenticated_user_failed_db_read():
    processor = ProcessGetByForAuthenticatedUser(mock_db_read_not_found, 'product', StubDataManager())
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


def mock_db_read(resource_id, auth_user_id, data_manager):
    product = Product()
    brand = Brand()
    brand.id = str(uuid.uuid4())
    product.brand = brand
    return product


def mock_db_read_not_found(resource_id, auth_user_id, data_manager):
    return None
