import json
import os

from _pytest.fixtures import fixture
from mock import patch, Mock

with patch.dict(os.environ, {'DATABASE_NAME': 'mock-value',
                             'DB_CLUSTER_ARN': 'mock-value',
                             'DB_SECRET_ARN': 'mock-value'}):
    from functions import app

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

my_data_path = os.path.join(THIS_DIR, os.pardir, '../events/')


@fixture
def good_product_with_logo():
    with open(my_data_path + 'create_brand.json') as f:
        data = json.load(f)
    return data


def test_app_to_controller(good_product_with_logo):
    mock_repository = Mock()
    mock_repository.create = Mock(return_value="id-123")
    app.util_web.util_db.Repository = mock_repository
    response = app.lambda_handler(good_product_with_logo, context=None)
    print(response)
    mock_repository.create.assert_called_once()
    assert response['statusCode'] == 201
    assert "/brands?id=id-123" in response['body']