from unittest.mock import patch

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.processors.feed import ProcessPublicFeed
from tests.unit import StubDataManager


@patch('src.processors.feed.load_brands')
@patch('src.processors.feed.load_max_3_products_for_brand')
def test_feed_processor_response_is_200(mock_load_brands, mock_load_max_3_products_for_brand):
    mock_load_brands.return_value = [Brand(), Brand()]
    mock_load_max_3_products_for_brand.return_value = [Product(), Product(), Product()]
    process_public_feed = ProcessPublicFeed(StubDataManager())
    pinfluencer_response = process_public_feed.do_process({})
    assert pinfluencer_response.is_ok() is True
