import os
import json
from mock import patch, Mock

with patch.dict(os.environ, {'DATABASE_NAME': 'mock-value',
                             'DB_CLUSTER_ARN': 'mock-value',
                             'DB_SECRET_ARN': 'mock-value'}):
    from functions import app

from _pytest.fixtures import fixture

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

my_data_path = os.path.join(THIS_DIR, os.pardir, '../events/')


@fixture
def get_feed():
    with open(my_data_path + 'get_feed.json') as f:
        data = json.load(f)
    return data


@fixture
def get_resource_unauth():
    with open(my_data_path + 'get_resource_unauth.json') as f:
        data = json.load(f)
    return data


@fixture
def post_resource_auth():
    with open(my_data_path + 'create_brand.json') as f:
        data = json.load(f)
    return data

@fixture
def post_resource_auth_without_body():
    with open(my_data_path + 'create_product_without_body.json') as f:
        data = json.load(f)
    return data


def test_get_feed(get_feed):
    app.util_web.Controller.do_process = Mock()
    app.lambda_handler(get_feed, None)
    app.util_web.Controller.do_process.assert_called_once_with('get', 'feed', None, None)


def test_get_resource(get_resource_unauth):
    app.util_web.Controller.do_process = Mock()
    app.lambda_handler(get_resource_unauth, None)
    app.util_web.Controller.do_process.assert_called_once_with('get', 'product', None, None)


def test_create_resource(post_resource_auth):
    app.util_web.Controller.do_process = Mock()
    app.lambda_handler(post_resource_auth, None)
    app.util_web.Controller.do_process.assert_called_once_with('post', 'brand', NotNone(), NotNone())


def test_create_resource_without_body(post_resource_auth_without_body):
    app.util_web.Controller.do_process = Mock()
    app.lambda_handler(post_resource_auth_without_body, None)
    app.util_web.Controller.do_process.assert_called_once_with('post', 'product', NotNone(), None)


class NotNone(object):
    def __eq__(a, b):
        return b is not None
