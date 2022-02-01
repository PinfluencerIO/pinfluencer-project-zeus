from unittest import TestCase

from src.data.repositories import BrandRepository
from tests import InMemorySqliteDataManager, brand_generator, brand_dto_generator


class BrandRepositoryTestCase(TestCase):

    def setUp(self):
        self._data_manager = InMemorySqliteDataManager()
        self._sut = BrandRepository(data_manager=self._data_manager)


class TestBaseRepository(BrandRepositoryTestCase):

    def test_load_by_id(self):
        expected_brand = brand_dto_generator(1)
        self._data_manager.create_fake_data([brand_generator(expected_brand)])
        actual_brand = self._sut.load_by_id(id_=expected_brand.id)
        assert expected_brand.__dict__ == actual_brand.__dict__

    def test_load_by_id_when_brand_cannot_be_found(self):
        actual_brand = self._sut.load_by_id(id_="1234")
        assert actual_brand is None

    def test_load_collection(self):
        expected_brands = [brand_dto_generator(1), brand_dto_generator(2), brand_dto_generator(3)]
        self._data_manager.create_fake_data(list(map(lambda x: brand_generator(x), expected_brands)))
        actual_brands = self._sut.load_collection()
        
        assert list(map(lambda x: x.__dict__, expected_brands)) == list(map(lambda x: x.__dict__, actual_brands))

    def test_load_collection_when_no_brands_exist(self):
        actual_brands = self._sut.load_collection()
        assert [] == actual_brands


class TestUserRepository(BrandRepositoryTestCase):

    def test_load_for_auth_user(self):
        expected = brand_dto_generator(num=1)
        self._data_manager.create_fake_data([brand_generator(expected)])
        actual = self._sut.load_for_auth_user(auth_user_id="1234brand1")
        assert expected.__dict__ == actual.__dict__

    def test_load_for_auth_user_when_brand_not_found(self):
        actual = self._sut.load_for_auth_user(auth_user_id="1234brand1")
        assert actual is None

    def test_write_new_for_auth_user(self):
        expected = brand_dto_generator(num=1)
        self._sut.write_new_for_auth_user(auth_user_id="1234brand1",
                                          payload=expected)
        actual = self._sut.load_by_id(id_=expected.id)
        assert actual.__dict__ == expected.__dict__