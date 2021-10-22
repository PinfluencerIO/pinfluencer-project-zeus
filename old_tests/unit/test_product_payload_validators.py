import json
import os

import pytest
from mock import patch
from _pytest.fixtures import fixture
from schema import SchemaError

with patch.dict(os.environ, {'DATABASE_NAME': 'mock-value',
                             'DB_CLUSTER_ARN': 'mock-value',
                             'DB_SECRET_ARN': 'mock-value'}):
    from functions.util_web import payload_validators


@fixture
def good_product():
    x = '{ "name":"product name", "description":"description", "requirements":"requirement 1, requirement 2, requirement 3"} '
    return json.loads(x)


@fixture
def bad_product():
    x = '{ "NAMED_WRONG":"product name", "description":"description", "requirement":"requirement 1, requirement 2, requirement 3"} '
    return json.loads(x)


@fixture
def good_product_with_product_image():
    x = '{ "name":"product name", "description":"description", "image": {"name":"filename.jpg", "bytes": "base64 encoded"}, "requirements":"requirement 1, requirement 2, requirement 3"}'
    return json.loads(x)


@fixture
def bad_product_with_partial_product_image():
    x = '{ "named":"product name", "description":"description", "image": {"name":"filename.jpg"}, "requirements":"requirement 1, requirement 2, requirement 3"} '
    return json.loads(x)


def test_valid_create_product_payload(good_product):
    payload_validators['post']['product'].validate(good_product)


def test_valid_create_product_with_product_image_payload(good_product_with_product_image):
    payload_validators['post']['product'].validate(good_product_with_product_image)


def test_invalid_create_product_with_partial_product_image_payload(bad_product_with_partial_product_image):
    with pytest.raises(SchemaError):
        payload_validators['post']['product'].validate(bad_product_with_partial_product_image)


def test_invalid_create_product_payload(bad_product):
    with pytest.raises(SchemaError):
        payload_validators['post']['product'].validate(bad_product)
