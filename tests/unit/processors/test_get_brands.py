from src.processors.get_brands import ProcessPublicBrands
from tests.unit import StubDataManager
from tests.unit.processors.test_brands import mock_load_brands


def test_process_public_brands_response_is_200():
    process_public_brands = ProcessPublicBrands(mock_load_brands, StubDataManager())
    pinfluencer_response = process_public_brands.do_process({})
    assert pinfluencer_response.is_ok() is True
