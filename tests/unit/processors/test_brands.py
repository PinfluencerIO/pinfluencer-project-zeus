from unittest.mock import patch

from src.processors.brands import ProcessPublicBrands
from tests.unit import StubDataManager


@patch('src.processors.brands.to_list')
def test_process_public_brands_response_is_200(mock_to_list):
    mock_to_list.return_value = [{}]
    process_public_brands = ProcessPublicBrands(StubDataManager())
    pinfluencer_response = process_public_brands.do_process({})
    assert pinfluencer_response.is_ok() is True
