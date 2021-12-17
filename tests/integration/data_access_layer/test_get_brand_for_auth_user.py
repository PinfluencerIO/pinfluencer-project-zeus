from src.data_access_layer.read_data_access import load_brand_for_authenticated_user
from tests.unit import InMemorySqliteDataManager, brand_generator


def test_load_brand_by_auth_id_item_when_brand_can_be_found():
    data_manager = InMemorySqliteDataManager()
    brand = brand_generator(1)
    data_manager.create_fake_data([brand])
    item = load_brand_for_authenticated_user(data_manager=data_manager, auth_user_id=brand.auth_user_id)
    assert brand.as_dict() == item.as_dict()


def test_load_brand_item_by_auth_id_when_brand_cannot_be_found():
    data_manager = InMemorySqliteDataManager()
    brand = brand_generator(1)
    data_manager.create_fake_data([brand])
    item = load_brand_for_authenticated_user(data_manager=data_manager, auth_user_id="invalid id")
    assert item is None


def test_load_brand_item_by_auth_id_when_no_brands_exist():
    data_manager = InMemorySqliteDataManager()
    item = load_brand_for_authenticated_user(data_manager=data_manager, auth_user_id="invalid id")
    assert item is None
