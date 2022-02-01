from unittest import TestCase

from src.data_access_layer.repositories import BrandRepository
from tests import InMemorySqliteDataManager, brand_generator, brand_dto_generator


class TestBaseRepository(TestCase):

    def setUp(self):
        self.__data_manager = InMemorySqliteDataManager()
        self.__repository = BrandRepository(data_manager=self.__data_manager, image_repository=None)

    def test_load_brand_by_id_item_when_brand_can_be_found(self):
        unexpected_brand = brand_dto_generator(1)
        self.__data_manager.create_fake_data([brand_generator(unexpected_brand)])
        actual_brand = self.__repository.load_by_id(id_=unexpected_brand.id)
        assert unexpected_brand.__dict__ == actual_brand.__dict__

    def test_load_brand_item_by_id_when_brand_cannot_be_found(self):
        actual_brand = self.__repository.load_by_id(id_="1234")
        assert actual_brand is None
