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
def good_brand():
    x = '{ "name":"brand name", ' \
        '"description":"description", ' \
        '"website":"www.name-of-brand.com", ' \
        '"email":"email@name-of-brand.com"}'
    return json.loads(x)


@fixture
def bad_brand():
    x = '{ "named":"brand name", ' \
        '"description":"description", ' \
        '"website":"www.name-of-brand.com", ' \
        '"email":"email@name-of-brand.com"}'
    return json.loads(x)


@fixture
def good_brand_with_logo():
    x = '{ "name":"brand name", ' \
        '"description":"description", ' \
        '"website":"www.name-of-brand.com", ' \
        '"email":"email@name-of-brand.com", ' \
        '"logo": ' \
        '   {' \
        '       "name":"logo-filename.jpg",' \
        '       "bytes":""' \
        '   }' \
        '}'
    return json.loads(x)


@fixture
def bad_brand_with_partial_logo():
    x = '{ "name":"brand name", ' \
        '"description":"description", ' \
        '"website":"www.name-of-brand.com", ' \
        '"email":"email@name-of-brand.com", ' \
        '"logo": {"name":"logo-filename.jpg"}}'
    return json.loads(x)


def test_valid_create_brand_payload(good_brand):
    payload_validators['brand'].validate(good_brand)


def test_valid_create_brand_with_logo_payload(good_brand_with_logo):
    payload_validators['brand'].validate(good_brand_with_logo)


def test_invalid_create_brand_with_partial_logo_payload(bad_brand_with_partial_logo):
    with pytest.raises(SchemaError):
        payload_validators['brand'].validate(bad_brand_with_partial_logo)


def test_invalid_create_brand_payload(bad_brand):
    with pytest.raises(SchemaError):
        payload_validators['brand'].validate(bad_brand)
