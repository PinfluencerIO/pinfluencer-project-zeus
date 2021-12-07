from unittest.mock import patch

import pytest

from src.data_access_layer.brand import Brand
from src.filters.authorised_filter import GetBrandAssociatedWithCognitoUser, OwnerOnly, NoBrandAssociatedWithCognitoUser
from tests.unit import StubDataManager

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


@patch('src.filters.authorised_filter.load_brand_by_auth_id')
def test_brand_found_for_cognito_user_and_added_to_event(mock_load):
    brand = Brand()
    mock_load.return_value = brand

    data_manager = StubDataManager()
    _filter = GetBrandAssociatedWithCognitoUser(data_manager)

    response = _filter.do_filter(event_cognito_user)

    assert response.is_success() is True
    assert response.get_code() == 200
    assert response.get_payload() == brand.as_dict()
    mock_load.assert_called_with(user_id, data_manager)


@patch('src.filters.authorised_filter.load_brand_by_auth_id')
def test_brand_not_found_for_cognito_user_response_with_401(mock_load):
    mock_load.return_value = None

    data_manager = StubDataManager()
    _filter = GetBrandAssociatedWithCognitoUser(data_manager)

    response = _filter.do_filter(event_cognito_user)

    assert response.is_success() is False
    assert response.get_code() == 401
    mock_load.assert_called_with(user_id, data_manager)


@patch('src.filters.authorised_filter.load_brand_by_auth_id')
def test_missing_cognito_user_response_with_401(mock_load):
    mock_load.return_value = None

    data_manager = StubDataManager()
    _filter = GetBrandAssociatedWithCognitoUser(data_manager)

    response = _filter.do_filter({})

    assert response.is_success() is False
    assert response.get_code() == 401


def test_when_missing_key_in_event_response_with_raising_key_error():
    _filter = OwnerOnly('product')

    with pytest.raises(KeyError):
        _filter.do_filter({})


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


def test_when_owner_owns_resource_response_with_200():
    _filter = OwnerOnly('product')

    response = _filter.do_filter(event_with_authorised_ownership)

    assert response.is_success()


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


def test_when_owner_is_not_authorised_for_resource_response_with_401():
    _filter = OwnerOnly('product')

    response = _filter.do_filter(event_with_mismatched_ids)

    assert response.is_success() is False
    assert response.get_code() == 401


@patch('src.filters.authorised_filter.load_brand_by_auth_id')
def test_brand_already_associated_with__user_response_with_400(mock_load):
    mock_load.return_value = Brand()

    data_manager = StubDataManager()
    _filter = NoBrandAssociatedWithCognitoUser(data_manager)

    response = _filter.do_filter(event_cognito_user)

    assert response.is_success() is False
    assert response.get_code() == 400
    mock_load.assert_called_with(user_id, data_manager)


@patch('src.filters.authorised_filter.load_brand_by_auth_id')
def test_brand_not_already_associated_with__user_response_with_200(mock_load):
    mock_load.return_value = None

    data_manager = StubDataManager()
    _filter = NoBrandAssociatedWithCognitoUser(data_manager)

    response = _filter.do_filter(event_cognito_user)

    assert response.is_success() is True
    assert response.get_code() == 200
    mock_load.assert_called_with(user_id, data_manager)
