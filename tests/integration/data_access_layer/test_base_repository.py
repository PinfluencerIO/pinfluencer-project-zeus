from unittest import TestCase

from src.data_access_layer.repositories import BrandRepository
from tests import InMemorySqliteDataManager, brand_generator, brand_dto_generator


class TestBaseRepository(TestCase):

    def setUp(self):
        self.__data_manager = InMemorySqliteDataManager()
        self.__repository = BrandRepository(data_manager=self.__data_manager, image_repository=None)

    def test_load_by_id(self):
        expected_brand = brand_dto_generator(1)
        self.__data_manager.create_fake_data([brand_generator(expected_brand)])
        actual_brand = self.__repository.load_by_id(id_=expected_brand.id)
        assert expected_brand.__dict__ == actual_brand.__dict__

    def test_load_by_id_when_brand_cannot_be_found(self):
        actual_brand = self.__repository.load_by_id(id_="1234")
        assert actual_brand is None

    def test_load_collection(self):
        expected_brands = [brand_dto_generator(1), brand_dto_generator(2), brand_dto_generator(3)]
        self.__data_manager.create_fake_data(list(map(lambda x: brand_generator(x), expected_brands)))
        actual_brands = self.__repository.load_collection()
        assert list(map(lambda x: x.__dict__, expected_brands)) == list(map(lambda x: x.__dict__, actual_brands))
