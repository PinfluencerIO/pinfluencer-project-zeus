import uuid

from src.data_access_layer.brand import Brand
from src.filters import FilterResponse
from src.processors.brands.get_brand_for_authenticated_user import ProcessGetAuthenticatedBrand
from tests.unit import StubDataManager
from tests.unit.processors.brands import MockFilterResponse


def test_process_authenticated_brand_success():
    brand = Brand()
    brand_id = str(uuid.uuid4())
    brand.id = brand_id
    successful_response_with_brand = FilterResponse('', 200, brand)
    get_brand_associated_with_cognito_user = MockFilterResponse(successful_response_with_brand)

    get_authenticated_process = ProcessGetAuthenticatedBrand(get_brand_associated_with_cognito_user,
                                                             StubDataManager())
    pinfluencer_response = get_authenticated_process.do_process({})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) == dict
    assert pinfluencer_response.body['id'] == brand_id


def test_process_authenticated_brand_failure_to_find_brand_associated_with_cognito_user():
    unsuccessful_response_with_brand = FilterResponse('', 404, {})
    get_brand_associated_with_cognito_user = MockFilterResponse(unsuccessful_response_with_brand)

    get_authenticated_process = ProcessGetAuthenticatedBrand(get_brand_associated_with_cognito_user,
                                                             StubDataManager())

    pinfluencer_response = get_authenticated_process.do_process({})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 404
