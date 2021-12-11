import pytest

from src.data_access_layer.brand import Brand
from src.filters import FilterResponse
from src.processors.brands.create_brand_for_authenticated_user import ProcessAuthenticatedPostBrand
from tests.unit import StubDataManager
from tests.unit.processors.brands import MockFilterResponse, event_cognito_user, mock_successful_db_call, \
    mock_db_call_with_exception


def test_process_new_brand_success():
    manager = StubDataManager()
    post_brand = ProcessAuthenticatedPostBrand(MockFilterResponse(FilterResponse('', 200, Brand().as_dict())),
                                               MockFilterResponse(FilterResponse('', 200, Brand().as_dict())),
                                               mock_successful_db_call,
                                               manager)

    pinfluencer_response = post_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is True


def test_process_new_brand_failed_already_associated_brand():
    manager = StubDataManager()
    post_brand = ProcessAuthenticatedPostBrand(MockFilterResponse(FilterResponse('', 400, Brand().as_dict())),
                                               MockFilterResponse(FilterResponse('', 200, Brand().as_dict())),
                                               mock_successful_db_call,
                                               manager)

    pinfluencer_response = post_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_new_brand_failed_invalid_brand_payload():
    manager = StubDataManager()
    post_brand = ProcessAuthenticatedPostBrand(MockFilterResponse(FilterResponse('', 200, Brand().as_dict())),
                                               MockFilterResponse(FilterResponse('', 400, Brand().as_dict())),
                                               mock_successful_db_call,
                                               manager)

    pinfluencer_response = post_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_new_brand_failed_write_brand():
    manager = StubDataManager()
    post_brand = ProcessAuthenticatedPostBrand(MockFilterResponse(FilterResponse('', 200, Brand().as_dict())),
                                               MockFilterResponse(FilterResponse('', 200, Brand().as_dict())),
                                               mock_db_call_with_exception,
                                               manager)

    with pytest.raises(Exception):
        post_brand.do_process(event_cognito_user)
