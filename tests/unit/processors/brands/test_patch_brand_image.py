import uuid

import pytest

from src.data_access_layer.brand import Brand
from src.filters import FilterResponse
from src.processors.brands.update_image_for_brand_of_authenticated_user import ProcessAuthenticatedPatchBrandImage
from tests.unit import StubDataManager
from tests.unit.processors.brands import MockFilterResponse, event_cognito_user, mock_successful_update_brand_image, \
    mock_update_brand_image_raise_exception


def test_process_patch_brand_image_success():
    manager = StubDataManager()
    brand = Brand()
    brand.id = str(uuid.uuid4())
    mock_get_brand_for_auth_user = MockFilterResponse(response=(FilterResponse('', 200, brand)))
    mock_validated_payload = MockFilterResponse(response=(FilterResponse('', 200, event_cognito_user['body'])))

    patch_brand_image = ProcessAuthenticatedPatchBrandImage(
        mock_get_brand_for_auth_user,
        mock_validated_payload,
        mock_successful_update_brand_image,
        manager)

    pinfluencer_response = patch_brand_image.do_process(event_cognito_user)

    assert pinfluencer_response.is_ok() is True


def test_process_patch_brand_image_failed_authentication():
    manager = StubDataManager()
    b = Brand()
    b.id = str(uuid.uuid4())
    mock_unsuccessful_filter = FilterResponse('', 401, {})
    success_filter_response = FilterResponse('', 200, b.as_dict())
    failed_to_get_brand_associated_with_cognito_user = MockFilterResponse(response=mock_unsuccessful_filter)
    mock_success_filter = MockFilterResponse(response=success_filter_response)

    patch_brand_image = ProcessAuthenticatedPatchBrandImage(
        failed_to_get_brand_associated_with_cognito_user,
        mock_success_filter,
        mock_successful_update_brand_image,
        manager)

    pinfluencer_response = patch_brand_image.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 401


def test_process_patch_brand_image_failed_validation():
    manager = StubDataManager()
    b = Brand()
    b.id = str(uuid.uuid4())
    get_brand_associated_with_cognito_user = MockFilterResponse(response=(FilterResponse('', 200, Brand())))
    mock_unsuccessful_validation = MockFilterResponse(response=(FilterResponse('', 400, {})))

    patch_brand_image = ProcessAuthenticatedPatchBrandImage(
        get_brand_associated_with_cognito_user,
        mock_unsuccessful_validation,
        mock_successful_update_brand_image,
        manager)

    pinfluencer_response = patch_brand_image.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_patch_brand_image_failed_update_brand_write():
    manager = StubDataManager()
    b = Brand()
    b.id = str(uuid.uuid4())
    get_brand_associated_with_cognito_user = MockFilterResponse(response=(FilterResponse('', 200, b.as_dict())))
    mock_successful_filter = MockFilterResponse(response=(FilterResponse('', 200, b.as_dict())))

    patch_brand_image = ProcessAuthenticatedPatchBrandImage(
        get_brand_associated_with_cognito_user,
        mock_successful_filter,
        mock_update_brand_image_raise_exception,
        manager)

    with pytest.raises(Exception):
        patch_brand_image.do_process(event_cognito_user)
