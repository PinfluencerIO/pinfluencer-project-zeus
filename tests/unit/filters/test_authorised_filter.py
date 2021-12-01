from unittest.mock import patch

from src.data_access_layer.brand import Brand
from src.web.filters.authorised_filter import AuthFilter
from tests.unit import FakeDataManager

user_id = 'user_id'
event = {
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


@patch('src.web.filters.authorised_filter.load_brand_by_auth_id')
def test_brand_found_for_cognito_user_and_added_to_event(mock_load):
    mock_load.return_value = Brand()

    data_manager = FakeDataManager()
    _filter = AuthFilter(data_manager)

    response = _filter.do_filter(event)

    assert response.is_success() is True
    assert response.get_code() == 200
    assert 'auth_brand' in event
    mock_load.assert_called_with(user_id, data_manager)


@patch('src.web.filters.authorised_filter.load_brand_by_auth_id')
def test_brand_not_found_for_cognito_user_response_with_401(mock_load):
    mock_load.return_value = None

    data_manager = FakeDataManager()
    _filter = AuthFilter(data_manager)

    response = _filter.do_filter(event)

    assert response.is_success() is False
    assert response.get_code() == 401
    mock_load.assert_called_with(user_id, data_manager)


@patch('src.web.filters.authorised_filter.load_brand_by_auth_id')
def test_missing_cognito_user_response_with_401(mock_load):
    mock_load.return_value = None

    data_manager = FakeDataManager()
    _filter = AuthFilter(data_manager)

    response = _filter.do_filter({})

    assert response.is_success() is False
    assert response.get_code() == 401
