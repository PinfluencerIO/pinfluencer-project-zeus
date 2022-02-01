from unittest import TestCase
from unittest.mock import Mock, MagicMock

from src.data_access_layer.repositories import BrandRepository
from tests import InMemorySqliteDataManager, brand_generator, brand_dto_generator


class TestUserRepository(TestCase):

    def setUp(self):
        self.__data_manager = InMemorySqliteDataManager()
        self.__image_repository = Mock()
        self.__sut = BrandRepository(data_manager=self.__data_manager,
                                     image_repository=self.__image_repository)

    def test_load_for_auth_user(self):
        expected = brand_dto_generator(num=1)
        self.__data_manager.create_fake_data([brand_generator(expected)])
        actual = self.__sut.load_for_auth_user(auth_user_id="1234brand1")
        assert expected.__dict__ == actual.__dict__

    def test_load_for_auth_user_when_brand_not_found(self):
        actual = self.__sut.load_for_auth_user(auth_user_id="1234brand1")
        assert None == actual

    def test_write_new_for_auth_user(self):
        self.__image_repository.upload = MagicMock(return_value="")
        expected = brand_dto_generator(num=1)
        self.__sut.write_new_for_auth_user(auth_user_id="1234brand1",
                                           payload=expected)

        assert self.__sut.load_by_id(id_=expected.id).__dict__ == expected.__dict__
        assert self.__data_manager.changes_were_committed_once()
