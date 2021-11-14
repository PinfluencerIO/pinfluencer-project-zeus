import pytest

from src.web.http_util import PinfluencerResponse
from src.web.processors.brands import ProcessPublicBrands
from tests.unit.fake_data_manager import FakeDataManager


@pytest.fixture()
def brand_processor():
    data_manager = FakeDataManager()
    brand_processor = ProcessPublicBrands(data_manager=data_manager)
    yield brand_processor


class WhenGetAllBrandsIsCalled:

    @staticmethod
    def when(brand_processor: ProcessPublicBrands) -> PinfluencerResponse:
        return brand_processor.do_process({})

    def then_200_response_is_returned(self, brand_processor: ProcessPublicBrands):
        assert self.when(brand_processor).is_ok()

    def then_3_brands_are_found(self, brand_processor: ProcessPublicBrands):
        assert len(self.when(brand_processor).body) == 3
