import uuid
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from src.routes import BrandController
from tests import brand_dto_generator


class TestBrandController(TestCase):

    def setUp(self):
        self.__brand_repository = Mock()
        self.__sut = BrandController(brand_repository=self.__brand_repository,
                                     data_manager=None,
                                     image_repo=None)

    def test_handle_get_by_id(self):
        brand = brand_dto_generator(num=1)
        self.__brand_repository.load_by_id = MagicMock(return_value=brand)
        pinfluencer_response = self.__sut.handle_get_by_id({'pathParameters': {'brand_id': brand.id}})
        self.__brand_repository.load_by_id.assert_called_once_with(id_=brand.id)
        assert pinfluencer_response.body == brand.__dict__
        assert pinfluencer_response.is_ok() is True

    def test_handle_get_by_id_when_brand_not_found(self):
        self.__brand_repository.load_by_id = MagicMock(return_value=None)
        field = str(uuid.uuid4())
        pinfluencer_response = self.__sut.handle_get_by_id({'pathParameters': {'brand_id': field}})
        self.__brand_repository.load_by_id.assert_called_once_with(id_=field)
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 404

    def test_handle_get_by_id_when_invalid_uuid(self):
        self.__brand_repository.load_by_id = MagicMock(return_value=None)
        field = "12345"
        pinfluencer_response = self.__sut.handle_get_by_id({'pathParameters': {'brand_id': field}})
        self.__brand_repository.load_by_id.assert_not_called()
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 400

    def test_handle_get_all_brands(self):
        expected_brands = [
            brand_dto_generator(num=1),
            brand_dto_generator(num=2),
            brand_dto_generator(num=3),
            brand_dto_generator(num=4)
        ]
        self.__brand_repository.load_collection = MagicMock(return_value=expected_brands)
        pinfluencer_response = self.__sut.handle_get_all_brands({})
        self.__brand_repository.load_collection.assert_called_once()
        assert pinfluencer_response.body == list(map(lambda x: x.__dict__, expected_brands))
        assert pinfluencer_response.status_code == 200

    def test_handle_get_brand(self):
        expected_brand = brand_dto_generator(num=1)
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=expected_brand)
        auth_id = "1234brand1"
        response = self.__sut.handle_get_brand({"requestContext": {"authorizer": {"jwt": {"claims":{"cognito:username": auth_id}}}}})
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)
        assert response.body == expected_brand.__dict__
        assert response.status_code == 200

    def test_handle_get_brand_when_brant_not_found(self):
        self.__brand_repository.load_for_auth_user = MagicMock(return_value=None)
        auth_id = "1234brand1"
        response = self.__sut.handle_get_brand({"requestContext": {"authorizer": {"jwt": {"claims":{"cognito:username": auth_id}}}}})
        self.__brand_repository.load_for_auth_user.assert_called_once_with(auth_user_id=auth_id)
        assert response.body == {}
        assert response.status_code == 404
