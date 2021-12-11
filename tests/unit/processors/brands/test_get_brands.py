from src.processors.brands.get_brands import ProcessPublicBrands
from tests.unit import StubDataManager
from tests.unit.processors.brands import mock_load_brands


def test_get_brands():
    process_public_brands = ProcessPublicBrands(mock_load_brands, StubDataManager())
    pinfluencer_response = process_public_brands.do_process({})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) == list
    assert len(pinfluencer_response.body) == 2
