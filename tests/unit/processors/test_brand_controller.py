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

    def test_public_get_by_id_for_brand(self):
        brand = brand_dto_generator(num=1)
        self.__brand_repository.load_by_id = MagicMock(return_value=brand)
        pinfluencer_response = self.__sut.handle_get_by_id({'pathParameters': {'brand_id': brand.id}})
        self.__brand_repository.load_by_id.assert_called_once_with(id_=brand.id)
        assert pinfluencer_response.body == brand.__dict__
        assert pinfluencer_response.is_ok() is True

    def test_public_get_by_id_for_brand_not_found(self):
        self.__brand_repository.load_by_id = MagicMock(return_value=None)
        field = str(uuid.uuid4())
        pinfluencer_response = self.__sut.handle_get_by_id({'pathParameters': {'brand_id': field}})
        self.__brand_repository.load_by_id.assert_called_once_with(id_=field)
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 404

    def test_public_get_by_id_for_brand_invalid_uuid(self):
        self.__brand_repository.load_by_id = MagicMock(return_value=None)
        field = "12345"
        pinfluencer_response = self.__sut.handle_get_by_id({'pathParameters': {'brand_id': field}})
        self.__brand_repository.load_by_id.assert_not_called()
        assert pinfluencer_response.body == {}
        assert pinfluencer_response.status_code == 404
