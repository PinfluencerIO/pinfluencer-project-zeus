from unittest.mock import patch

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.processors.feed import ProcessPublicFeed
from tests.unit import StubDataManager
from tests.unit.processors.test_brands import mock_load_brands, mock_load_max_3_products_for_brand


def test_feed_processor_response_is_200():
    process_public_feed = ProcessPublicFeed(mock_load_brands, mock_load_max_3_products_for_brand, StubDataManager())
    pinfluencer_response = process_public_feed.do_process({})
    assert pinfluencer_response.is_ok() is True
