import uuid

from src.data_access_layer.write_data_access import NotFoundException
from src.processors.delete_product import ProcessAuthenticatedDeleteProduct
from tests.unit import StubDataManager


def test_do_process_product_delete():
    processor = ProcessAuthenticatedDeleteProduct(mock_delete_product, StubDataManager())
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


def test_do_process_product_delete_failed_product_id_validation():
    processor = ProcessAuthenticatedDeleteProduct(mock_delete_product, StubDataManager())
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


def test_do_process_product_delete_not_found():
    processor = ProcessAuthenticatedDeleteProduct(mock_delete_product_not_found, StubDataManager())
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


def mock_delete_product(auth_user_id, product_id, data_manager):
    pass


def mock_delete_product_not_found(auth_user_id, product_id, data_manager):
    raise NotFoundException('')
