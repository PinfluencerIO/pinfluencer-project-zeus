import pytest

from src.data_access_layer.brand import Brand
from src.web.http_util import PinfluencerResponse
from src.web.processors.brands import ProcessPublicBrands
from tests.unit import FakeDataManager, brand_generator


@pytest.fixture()
def get_public_brands_fixture():
    data_manager = FakeDataManager()
    brand_processor = ProcessPublicBrands(data_manager=data_manager)
    return brand_processor, data_manager


class TestPublicBrands:
    __result: PinfluencerResponse
    __brands: list[Brand]
    __brand_processor: ProcessPublicBrands
    __data_manager: FakeDataManager

    def __setup(self, get_public_brands_fixture, callback=lambda *args: None):
        (self.__brand_processor, self.__data_manager) = get_public_brands_fixture
        callback()
        self.__result = self.__brand_processor.do_process({})

    def __setup_test_data(self):
        self.__brands = [
            brand_generator(1),
            brand_generator(2),
            brand_generator(3)
        ]
        self.__data_manager.create_fake_data(self.__brands)

    def test_3_brands_are_found_when_db_is_populated(self, get_public_brands_fixture):
        self.__setup(get_public_brands_fixture, self.__setup_test_data)
        assert self.__result.is_ok()
        length = 3
        assert len(self.__result.body) == length
        for i in range(length):
            assert self.__brands[i].as_dict() == self.__result.body[i]

    def test_0_brands_are_found_when_db_is_empty(self, get_public_brands_fixture):
        self.__setup(get_public_brands_fixture)
        assert self.__result.is_ok()
        assert len(self.__result.body) == 0
