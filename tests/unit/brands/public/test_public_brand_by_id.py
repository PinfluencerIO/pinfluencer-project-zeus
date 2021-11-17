import uuid

import pytest

from src.data_access_layer.brand import Brand
from src.web.filters import FilterChainImp, ValidBrandId, NotFoundById
from src.web.http_util import PinfluencerResponse
from src.web.processors.brands import ProcessPublicGetBrandBy
from tests.unit import FakeDataManager, brand_generator


@pytest.fixture()
def get_public_brand_by_id_fixture():
    data_manager = FakeDataManager()
    brand_processor = ProcessPublicGetBrandBy(data_manager=data_manager, filter_chain=FilterChainImp([ValidBrandId(
        data_manager=data_manager
    )]))
    return brand_processor, data_manager


class TestPublicBrandById:
    __result: PinfluencerResponse
    __brands: list[Brand]
    __brand_processor: ProcessPublicGetBrandBy
    __data_manager: FakeDataManager
    __event: dict

    def __setup(self, get_public_brand_by_id_fixture, callback=lambda *args: None):
        (self.__brand_processor, self.__data_manager) = get_public_brand_by_id_fixture
        callback()
        self.__brand_processor.run_filters(event=self.__event)
        self.__result = self.__brand_processor.do_process(self.__event)

    def __setup_test_data(self):
        self.__brands = [
            brand_generator(1)
        ]
        self.__data_manager.create_fake_data(self.__brands)
        self.__event = {
            'pathParameters': {
                'brand_id': self.__brands[0].id
            }
        }

    def __setup_empty_data(self):
        self.__event = {
            'pathParameters': {
                'brand_id': str(uuid.uuid4())
            }
        }

    def test_correct_brand_is_found_when_brand_is_in_db(self, get_public_brand_by_id_fixture):
        self.__setup(get_public_brand_by_id_fixture=get_public_brand_by_id_fixture, callback=self.__setup_test_data)
        assert self.__result.is_ok()
        assert self.__result.body == self.__brands[0].as_dict()

    def test_no_brand_is_found_when_brand_is_not_in_db(self, get_public_brand_by_id_fixture):
        with pytest.raises(NotFoundById):
            self.__setup(get_public_brand_by_id_fixture=get_public_brand_by_id_fixture,
                         callback=self.__setup_empty_data)
