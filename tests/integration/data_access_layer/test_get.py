from src.data_access_layer.read_data_access import load_item
from src.processors import types
from tests.unit import InMemorySqliteDataManager, brand_generator


def test_load_brand_item_when_brand_exists():
    data_manager = InMemorySqliteDataManager()
    brand = brand_generator(1)
    data_manager.create_fake_data([brand])
    item = load_item(resource=types['brand']['type'], data_manager=data_manager)
    assert brand.as_dict() == item.as_dict()


def test_load_brand_item_when_no_brands_exist():
    data_manager = InMemorySqliteDataManager()
    item = load_item(resource=types['brand']['type'], data_manager=data_manager)
    assert item is None
