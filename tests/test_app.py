import os
from unittest import mock

from src.app import lambda_handler


@mock.patch.dict(os.environ, {'IN_MEMORY': 'True'})
def test_lambda_handler():

    response = lambda_handler({"routeKey": "GET /feed"}, {})
    print(f'response {response}')
    assert response['statusCode'] == 200
