import uuid

import pytest

from src.data_access_layer.brand import Brand
from src.filters import FilterResponse
from src.processors import protect_email_from_update_if_held_in_claims
from src.processors.brands.update_brand_for_authenticated_user import ProcessAuthenticatedPutBrand
from tests.unit import StubDataManager
from tests.unit.processors.brands import mock_successful_db_call, MockFilterResponse, event_cognito_user, email, \
    mock_db_call_with_exception


def test_process_update_brand_success():
    manager = StubDataManager()
    brand = Brand()
    brand.id = str(uuid.uuid4())
    put_brand = ProcessAuthenticatedPutBrand(MockFilterResponse(FilterResponse('', 200, brand)),
                                             MockFilterResponse(FilterResponse('', 200, event_cognito_user['body'])),
                                             mock_successful_db_call,
                                             manager)
    pinfluencer_response = put_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is True


def test_process_update_brand_success_with_email_in_claim():
    protect_email_from_update_if_held_in_claims(event_cognito_user['body'], event_cognito_user)
    assert event_cognito_user['body']['email'] == email


def test_process_update_brand_failed_authentication():
    manager = StubDataManager()
    brand = Brand()
    brand.id = str(uuid.uuid4())
    put_brand = ProcessAuthenticatedPutBrand(MockFilterResponse(FilterResponse('', 401, {})),
                                             MockFilterResponse(FilterResponse('', 200, brand.as_dict())),
                                             mock_successful_db_call,
                                             manager)
    pinfluencer_response = put_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 401


def test_process_update_brand_failed_invalid_payload():
    manager = StubDataManager()
    brand = Brand()
    brand.id = str(uuid.uuid4())
    put_brand = ProcessAuthenticatedPutBrand(MockFilterResponse(FilterResponse('', 200, brand)),
                                             MockFilterResponse(FilterResponse('', 400, {})),
                                             mock_successful_db_call,
                                             manager)
    pinfluencer_response = put_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_update_brand_failed_update_brand():
    manager = StubDataManager()
    brand = Brand()
    brand.id = str(uuid.uuid4())
    put_brand = ProcessAuthenticatedPutBrand(MockFilterResponse(FilterResponse('', 200, brand.as_dict())),
                                             MockFilterResponse(FilterResponse('', 200, brand.as_dict())),
                                             mock_db_call_with_exception,
                                             manager)

    with pytest.raises(Exception):
        put_brand.do_process(event_cognito_user)
