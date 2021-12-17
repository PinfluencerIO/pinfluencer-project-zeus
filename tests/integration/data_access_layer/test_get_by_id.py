import uuid

from src.data_access_layer.read_data_access import load_by_id
from src.processors import types
from tests.unit import InMemorySqliteDataManager, brand_generator


def test_load_brand_by_id_item_when_brand_exists():
    data_manager = InMemorySqliteDataManager()
    brand = brand_generator(1)
    data_manager.create_fake_data([brand])
    item = load_by_id(resource=types['brand']['type'], data_manager=data_manager, id_=brand.id)
    assert brand.as_dict() == item.as_dict()


def test_load_brand_item_by_id_when_brand_cannot_be_found():
    data_manager = InMemorySqliteDataManager()
    item = load_by_id(resource=types['brand']['type'], data_manager=data_manager, id_=str(uuid.uuid4()))
    assert item is None
