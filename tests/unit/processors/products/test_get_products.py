from src.processors.products.get_products import ProcessPublicProducts
from tests.unit import StubDataManager
from tests.unit.processors.products import mock_load_products


def test_all_products():
    processor = ProcessPublicProducts(mock_load_products, StubDataManager())

    pinfluencer_response = processor.do_process({})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) is list
    assert len(pinfluencer_response.body) is 2
