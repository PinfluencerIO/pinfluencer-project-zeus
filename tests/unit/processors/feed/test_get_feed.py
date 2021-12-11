from src.processors.feed.get_feed import ProcessPublicFeed
from tests.unit import StubDataManager
from tests.unit.processors.brands import mock_load_brands
from tests.unit.processors.feed import mock_load_max_3_products_for_brand


def test_feed_processor_response_is_200():
    process_public_feed = ProcessPublicFeed(mock_load_brands, mock_load_max_3_products_for_brand, StubDataManager())
    pinfluencer_response = process_public_feed.do_process({})
    assert pinfluencer_response.is_ok() is True
    assert type(pinfluencer_response.body) == list
    assert len(pinfluencer_response.body) == 6
