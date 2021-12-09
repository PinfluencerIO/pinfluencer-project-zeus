import uuid

import pytest

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.filters import FilterResponse, FilterInterface
from src.filters.authorised_filter import GetBrandAssociatedWithCognitoUser, NoBrandAssociatedWithCognitoUser
from src.filters.payload_validation import BrandPostPayloadValidation, BrandPutPayloadValidation
from src.processors.create_brand_for_authenticated_user import ProcessAuthenticatedPostBrand
from src.processors.get_brand_for_authenticated_user import ProcessAuthenticatedGetBrand
from src.processors.update_brand_for_authenticated_user import ProcessAuthenticatedPutBrand
from src.processors.update_image_for_brand_of_authenticated_user import ProcessAuthenticatedPatchBrandImage
from tests.unit import StubDataManager

user_id = 'user_id'
email = 'do@notupdate.email'
event_cognito_user = {
    'requestContext': {
        'authorizer': {
            'jwt': {
                'claims': {
                    'cognito:username': user_id,
                    'email': email
                }
            }
        }
    },
    'body': {
        'image': 'image bytes',
        'email': 'new@email.should.not.update.com'
    }
}


def test_process_authenticated_brand_success():
    authenticated_get_brand = ProcessAuthenticatedGetBrand(GetBrandAssociatedWithCognitoUser(StubDataManager()),
                                                           StubDataManager())
    authenticated_get_brand.get_authenticated_brand = mock_get_authenticated_brand_success
    pinfluencer_response = authenticated_get_brand.do_process({})
    assert pinfluencer_response.is_ok() is True


def test_process_authenticated_brand_failure():
    authenticated_get_brand = ProcessAuthenticatedGetBrand(GetBrandAssociatedWithCognitoUser(StubDataManager()),
                                                           StubDataManager())
    authenticated_get_brand.get_authenticated_brand = mock_get_authenticated_brand_failure
    pinfluencer_response = authenticated_get_brand.do_process({})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 404


def test_process_new_brand_success():
    manager = StubDataManager()
    post_brand = ProcessAuthenticatedPostBrand(NoBrandAssociatedWithCognitoUser(manager),
                                               BrandPostPayloadValidation(),
                                               manager)
    post_brand.check_no_brand_associated_with_authenticated_user = mock_no_brand_associated_with_authenticated_user
    post_brand.validate_new_brand_payload = mock_valid_brand_payload
    post_brand.create_new_brand = mock_create_new_brand_successful

    pinfluencer_response = post_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is True


def test_process_new_brand_failed_already_associated_brand():
    manager = StubDataManager()
    post_brand = ProcessAuthenticatedPostBrand(NoBrandAssociatedWithCognitoUser(manager), BrandPostPayloadValidation(),
                                               manager)
    post_brand.check_no_brand_associated_with_authenticated_user = mock_brand_associated_with_authenticated_user

    pinfluencer_response = post_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_new_brand_failed_invalid_brand_payload():
    manager = StubDataManager()
    post_brand = ProcessAuthenticatedPostBrand(NoBrandAssociatedWithCognitoUser(manager), BrandPostPayloadValidation(),
                                               manager)
    post_brand.check_no_brand_associated_with_authenticated_user = mock_no_brand_associated_with_authenticated_user
    post_brand.validate_new_brand_payload = mock_invalid_brand_payload

    pinfluencer_response = post_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_new_brand_failed_write_brand():
    manager = StubDataManager()
    post_brand = ProcessAuthenticatedPostBrand(NoBrandAssociatedWithCognitoUser(manager), BrandPostPayloadValidation(),
                                               manager)
    post_brand.check_no_brand_associated_with_authenticated_user = mock_no_brand_associated_with_authenticated_user
    post_brand.validate_new_brand_payload = mock_valid_brand_payload
    post_brand.create_new_brand = mock_failed_create_new_brand_successful

    with pytest.raises(Exception):
        post_brand.do_process(event_cognito_user)


def test_process_update_brand_success():
    manager = StubDataManager()
    put_brand = ProcessAuthenticatedPutBrand(GetBrandAssociatedWithCognitoUser(manager),
                                             BrandPutPayloadValidation(),
                                             manager)
    put_brand.call_get_brand_associated_with_cognito_user = mock_get_brand_associated_with_authenticated_user
    put_brand.validate_update_brand_payload = mock_valid_update_brand_payload
    put_brand.update_brand = mock_update_brand_successful

    pinfluencer_response = put_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is True


def test_process_update_brand_success_with_email_in_claim():
    manager = StubDataManager()
    put_brand = ProcessAuthenticatedPutBrand(GetBrandAssociatedWithCognitoUser(manager),
                                             BrandPutPayloadValidation(),
                                             manager)
    put_brand.call_get_brand_associated_with_cognito_user = mock_get_brand_associated_with_authenticated_user
    put_brand.validate_update_brand_payload = mock_valid_update_brand_payload
    put_brand.update_brand = mock_update_brand_successful

    pinfluencer_response = put_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is True


def test_process_update_brand_failed_authentication():
    manager = StubDataManager()
    put_brand = ProcessAuthenticatedPutBrand(GetBrandAssociatedWithCognitoUser(manager),
                                             BrandPutPayloadValidation(),
                                             manager)
    put_brand.call_get_brand_associated_with_cognito_user = mock_failed_to_get_associated_cognito_user

    pinfluencer_response = put_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 401


def test_process_update_brand_failed_invalid_payload():
    manager = StubDataManager()
    put_brand = ProcessAuthenticatedPutBrand(GetBrandAssociatedWithCognitoUser(manager),
                                             BrandPutPayloadValidation(),
                                             manager)
    put_brand.must_be_authenticated = mock_get_authenticated_brand_success
    put_brand.validate_update_brand_payload = mock_invalid_update_brand_payload

    pinfluencer_response = put_brand.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_update_brand_failed_update_brand():
    manager = StubDataManager()
    put_brand = ProcessAuthenticatedPutBrand(GetBrandAssociatedWithCognitoUser(manager),
                                             BrandPutPayloadValidation(),
                                             manager)
    put_brand.must_be_authenticated = mock_get_authenticated_brand_success
    put_brand.validate_update_brand_payload = mock_valid_update_brand_payload
    put_brand.update_brand = mock_failed_update_brand

    with pytest.raises(Exception):
        put_brand.do_process(event_cognito_user)


def test_process_patch_brand_image_success():
    manager = StubDataManager()
    patch_brand_image = ProcessAuthenticatedPatchBrandImage(
        MockAuthFilter(success=True),
        MockBrandImagePatchPayloadValidation(success=True),
        mock_successful_update_brand_image,
        manager)
    pinfluencer_response = patch_brand_image.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is True


def test_process_patch_brand_image_failed_authentication():
    manager = StubDataManager()
    patch_brand_image = ProcessAuthenticatedPatchBrandImage(
        MockAuthFilter(success=False),
        MockBrandImagePatchPayloadValidation(success=False),
        mock_successful_update_brand_image,
        manager)
    pinfluencer_response = patch_brand_image.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_patch_brand_image_failed_validation():
    manager = StubDataManager()
    patch_brand_image = ProcessAuthenticatedPatchBrandImage(
        MockAuthFilter(success=True),
        MockBrandImagePatchPayloadValidation(success=False),
        mock_successful_update_brand_image,
        manager)
    pinfluencer_response = patch_brand_image.do_process(event_cognito_user)
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400


def test_process_patch_brand_image_failed_update_brand_write():
    manager = StubDataManager()
    patch_brand_image = ProcessAuthenticatedPatchBrandImage(
        MockAuthFilter(success=True),
        MockBrandImagePatchPayloadValidation(success=True),
        mock_unsuccessful_update_brand_image,
        manager)

    with pytest.raises(Exception):
        patch_brand_image.do_process(event_cognito_user)


def mock_no_brand_associated_with_authenticated_user(event):
    return FilterResponse('', 200, {})


def mock_brand_associated_with_authenticated_user(event):
    return FilterResponse('', 400, {})


def mock_get_brand_associated_with_authenticated_user(event):
    return FilterResponse('', 200, Brand().as_dict())


def mock_failed_to_get_associated_cognito_user(event):
    return FilterResponse('', 404, {})


def mock_valid_brand_payload(event):
    return FilterResponse('', 200, event_cognito_user['body'])


def mock_valid_update_brand_payload(event):
    return FilterResponse('', 200, event_cognito_user['body'])


def mock_invalid_update_brand_payload(event):
    return FilterResponse('', 400, event_cognito_user['body'])


def mock_invalid_brand_payload(event):
    return FilterResponse('', 400, event_cognito_user['body'])


def mock_load_brands(data_manager):
    return [Brand(), Brand()]


def mock_load_max_3_products_for_brand(brand_id, data_manager):
    brand = Brand()
    brand.id = str(uuid.uuid4())
    product1 = Product()
    product1.brand = brand
    product2 = Product()
    product2.brand = brand
    product3 = Product()
    product3.brand = brand
    return [product1, product2, product3]


def mock_create_new_brand_successful(payload, image_bytes):
    return Brand()


def mock_update_brand_successful(id, payload):
    assert payload['email'] == email
    return Brand()


def mock_failed_create_new_brand_successful(payload, image_bytes):
    raise Exception()


def mock_failed_update_brand(id, payload):
    raise Exception()


def mock_get_authenticated_brand_failure(event):
    return FilterResponse('', 401, {})


def mock_get_authenticated_brand_success(event):
    brand = Brand()
    brand.id = str(uuid.uuid4())
    return FilterResponse('', 200, brand.as_dict())


class MockAuthFilter(FilterInterface):
    def __init__(self, success) -> None:
        super().__init__()
        self.success = success

    def do_filter(self, event: dict) -> FilterResponse:
        if self.success:
            return FilterResponse('', 200, Brand().as_dict())
        else:
            return FilterResponse('', 400, {})


class MockBrandImagePatchPayloadValidation(FilterInterface):

    def __init__(self, success) -> None:
        super().__init__()
        self.success = success

    def do_filter(self, event: dict) -> FilterResponse:
        if self.success:
            return FilterResponse('', 200, event['body'])
        else:
            return FilterResponse('', 400, {})


def mock_successful_update_brand_image(brand_id, image_bytes, data_manager):
    return Brand()


def mock_unsuccessful_update_brand_image(brand_id, image_bytes, data_manager):
    raise Exception('failed to write brand image')


class MockLoadResourcesId:
    def __init__(self, return_value: FilterResponse = None):
        self.return_value = return_value

    def load(self, dict):
        return self.return_value


def mock_load_all_products_for_brand_id(brand_id, data_manager):
    return mock_load_max_3_products_for_brand(brand_id, data_manager)