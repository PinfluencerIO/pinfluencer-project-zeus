from src.data_access_layer.brand import Brand
from src.filters.authorised_filter import GetBrandAssociatedWithCognitoUser, NoBrandAssociatedWithCognitoUser
from tests.unit import StubDataManager
from tests.unit.filters import mock_load_brand_by_auth_id, mock_failed_to_load_brand_by_auth_id

user_id = 'user_id'
event_cognito_user = {
    'requestContext': {
        'authorizer': {
            'jwt': {
                'claims': {
                    'cognito:username': user_id
                }
            }
        }
    }
}

_id = 'id'
event_with_authorised_ownership = {
    'product': {
        'brand': {
            'id': _id
        }
    },
    'auth_brand': {
        'id': _id
    }
}

event_with_mismatched_ids = {
    'product': {
        'id': 'product id',
        'brand': {
            'id': _id
        }
    },
    'auth_brand': {
        'id': 'other id'
    }
}


def test_get_brand_for_cognito_user():
    data_manager = StubDataManager()
    _filter = GetBrandAssociatedWithCognitoUser(mock_load_brand_by_auth_id, data_manager)

    response = _filter.do_filter(event_cognito_user)

    assert response.is_success() is True
    assert response.get_code() == 200
    assert type(response.get_payload()) == Brand


def test_brand_not_found_for_cognito_user_response_with_401():
    data_manager = StubDataManager()
    _filter = GetBrandAssociatedWithCognitoUser(mock_failed_to_load_brand_by_auth_id, data_manager)

    response = _filter.do_filter(event_cognito_user)

    assert response.is_success() is False
    assert response.get_code() == 401


def test_missing_cognito_user_response_with_400():
    data_manager = StubDataManager()
    _filter = GetBrandAssociatedWithCognitoUser(mock_failed_to_load_brand_by_auth_id, data_manager)

    response = _filter.do_filter({})

    assert response.is_success() is False
    assert response.get_code() == 400


def test_brand_already_associated_with__user_response_with_400():
    data_manager = StubDataManager()
    _filter = NoBrandAssociatedWithCognitoUser(mock_load_brand_by_auth_id, data_manager)

    response = _filter.do_filter(event_cognito_user)

    assert response.is_success() is False
    assert response.get_code() == 400


def test_brand_not_already_associated_with__user_response_with_200():
    data_manager = StubDataManager()
    _filter = NoBrandAssociatedWithCognitoUser(mock_failed_to_load_brand_by_auth_id, data_manager)

    response = _filter.do_filter(event_cognito_user)

    assert response.is_success() is True
    assert response.get_code() == 200
