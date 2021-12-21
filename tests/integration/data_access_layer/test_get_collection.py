from src.data_access_layer import to_list
from src.data_access_layer.read_data_access import load_collection
from src.processors import types
from tests import brand_generator, InMemorySqliteDataManager


def test_load_brand_collection_when_brands_exists():
    data_manager = InMemorySqliteDataManager()
    brands = [brand_generator(2), brand_generator(1)]
    data_manager.create_fake_data(brands)
    collection = load_collection(resource=types['brand']['type'], data_manager=data_manager)
    assert to_list(brands) == to_list(collection)


def test_load_brand_collection_when_no_brands_exists():
    data_manager = InMemorySqliteDataManager()
    collection = load_collection(resource=types['brand']['type'], data_manager=data_manager)
    assert [] == to_list(collection)
