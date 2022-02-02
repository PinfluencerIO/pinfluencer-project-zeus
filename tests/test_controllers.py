import json
import uuid
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from callee import Matching

from src.web.controllers import BrandController
from tests import brand_dto_generator


def get_brand_id_event(brand_id):
    return {'pathParameters': {'brand_id': brand_id}}


def get_auth_user_event(auth_id):
    return {"requestContext": {"authorizer": {"jwt": {"claims": {"cognito:username": auth_id}}}}}


def create_brand_for_auth_user_event(auth_id):
    return {
        "requestContext": {"authorizer": {"jwt": {"claims": {"cognito:username": auth_id}}}},
        "body": ""
    }


def create_event_body(expected):
    event = create_brand_for_auth_user_event(auth_id=expected.auth_user_id)
    expected_dict = dict(expected.__dict__)
    expected_dict['values'] = list(map(lambda x: x.name, expected.values))
    expected_dict['categories'] = list(map(lambda x: x.name, expected.categories))
    event['body'] = json.dumps(expected_dict, default=str)
    print(event)
    return event


class TestBrandController(TestCase):

    def setUp(self):
        self.__brand_repository = Mock()
        self.__sut = BrandController(brand_repository=self.__brand_repository)

    def test_get_by_id(self):
        brand = brand_dto_generator(num=1)
        self.__brand_repository.load_by_id = MagicMock(return_value=brand)
        pinfluencer_response = self.__sut.get_by_id(get_brand_id_event(brand.id))
        self.__brand_repository.load_by_id.assert_called_once_with(id_=brand.id)
        assert pinfluencer_response.body == brand.__dict__
        assert pinfluencer_response.is_ok() is True

    def test_get_by_id_when_not_found(self):
        self.__brand_repository.load_by_id = MagicMock(return_value=None)
        field = str(uuid.uuid4())
        pinfluencer_response = self.__sut.get_by_id(get_brand_id_event(field))
        self.__brand_repository.load_by_id.assert_called_once_with(id_=field)
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 404

    def test_get_by_id_when_invalid_uuid(self):
        self.__brand_repository.load_by_id = MagicMock(return_value=None)
        field = "12345"
        pinfluencer_response = self.__sut.get_by_id(get_brand_id_event(field))
        self.__brand_repository.load_by_id.assert_not_called()
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 400

    def test_get_all(self):
        expected_brands = [
            brand_dto_generator(num=1),
            brand_dto_generator(num=2),
            brand_dto_generator(num=3),
            brand_dto_generator(num=4)
        ]
        self.__brand_repository.load_collection = MagicMock(return_value=expected_brands)
        pinfluencer_response = self.__sut.get_all({})
        self.__brand_repository.load_collection.assert_called_once()
        assert pinfluencer_response.body == list(map(lambda x: x.__dict__, expected_brands))
        assert pinfluencer_response.status_code == 200

    def test_get(self):
        expected_brand = brand_dto_generator(num=1)
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=expected_brand)
        auth_id = "1234brand1"
        response = self.__sut.get(get_auth_user_event(auth_id))
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)
        assert response.body == expected_brand.__dict__
        assert response.status_code == 200

    def test_get_when_not_found(self):
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=None)
        auth_id = "1234brand1"
        response = self.__sut.get(get_auth_user_event(auth_id))
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)
        assert response.body == {}
        assert response.status_code == 404

    def test_create(self):

        expected = brand_dto_generator(num=1)
        self.__brand_repository.write_new_for_auth_user = MagicMock()
        event = create_event_body(expected)
        self.__sut.create(event=event)
        self.__brand_repository.write_new_for_auth_user.assert_called_once_with(auth_user_id=expected.auth_user_id,
                                                                                payload=Matching(lambda x: x.__dict__ == expected.__dict__))
