import os
import pytest
from mock import patch

with patch.dict(os.environ, {'DATABASE_NAME': 'mock-value', 'DB_CLUSTER_ARN': 'mock-value', 'DB_SECRET_ARN': 'mock-value'}):
    import functions.util_web as web


@pytest.fixture()
def goodEvent():
    return {"requestContext": {"http": {"method": "GET"}}}

@pytest.fixture()
def badEvent():
    return {"requestContext": {"http": {"missingMethod": "GET"}}}


def test_extract_http_method(goodEvent):
    method = web.Controller.extract_http_method(goodEvent)
    assert method == 'get'


def test_extract_http_method_fails(badEvent):
    with pytest.raises(Exception) as execinfo:
        web.Controller.extract_http_method(badEvent)
    assert execinfo.value.args[0] == 'method'

