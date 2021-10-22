import os
from mock import patch

with patch.dict(os.environ, {'DATABASE_NAME': 'mock-value',
                             'DB_CLUSTER_ARN': 'mock-value',
                             'DB_SECRET_ARN': 'mock-value'}):
    from functions import util_web


def test_http_util_response_for_success_200():
    response = util_web.HttpUtils.respond(None, 200, {'k': 'v'})
    assert response['statusCode'] == 200
    assert response['body'] == '{"k": "v"}'
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['headers']['Access-Control-Allow-Origin'] == '*'


def test_http_util_response_for_success_non_200():
    response = util_web.HttpUtils.respond(None, 201, {'k': 'v'})
    assert response['statusCode'] == 201
    assert response['body'] == '{"k": "v"}'
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['headers']['Access-Control-Allow-Origin'] == '*'


def test_http_util_response_for_error():
    response = util_web.HttpUtils.respond('ERROR', 400, {'k': 'v'})
    assert response['statusCode'] == 400
    assert response['body'] == 'ERROR'
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['headers']['Access-Control-Allow-Origin'] == '*'
