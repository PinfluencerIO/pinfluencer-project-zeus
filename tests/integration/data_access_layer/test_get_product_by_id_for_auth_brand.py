import uuid

from src.data_access_layer.read_data_access import load_product_by_id_for_auth_id
from tests import InMemorySqliteDataManager, brand_generator, product_generator


def test_load_product_by_id_for_brand_when_product_can_be_found_and_belongs_to_brand():
    [data_manager, products, brand] = setup_database()
    item = load_product_by_id_for_auth_id(data_manager=data_manager, auth_user_id=brand.auth_user_id,
                                          product_id=products[0].id)
    assert products[0].as_dict() == item.as_dict()


def test_load_product_by_id_for_brand_when_product_cannot_be_found():
    [data_manager, _, brand] = setup_database()
    item = load_product_by_id_for_auth_id(data_manager=data_manager, auth_user_id=brand.auth_user_id,
                                          product_id=str(uuid.uuid4()))
    assert item is None


def test_load_product_by_id_for_brand_when_product_doesnt_belong_to_brand():
    [data_manager, products, brand] = setup_database()
    item = load_product_by_id_for_auth_id(data_manager=data_manager, auth_user_id=brand.auth_user_id,
                                          product_id=products[2].id)
    assert item is None


def test_load_product_by_id_for_brand_when_no_products_exist():
    data_manager = InMemorySqliteDataManager()
    brand = brand_generator(1)
    data_manager.create_fake_data([brand])
    item = load_product_by_id_for_auth_id(data_manager=data_manager, auth_user_id=brand.auth_user_id,
                                          product_id=str(uuid.uuid4()))
    assert item is None


def test_load_product_by_id_for_brand_when_no_brands_exist():
    data_manager = InMemorySqliteDataManager()
    item = load_product_by_id_for_auth_id(data_manager=data_manager, auth_user_id="some auth id",
                                          product_id=str(uuid.uuid4()))
    assert item is None


def setup_database():
    data_manager = InMemorySqliteDataManager()
    brand = brand_generator(1)
    brand2 = brand_generator(2)
    products = [product_generator(1, brand), product_generator(2, brand), product_generator(3, brand2)]
    data_manager.create_fake_data([brand, brand2])
    data_manager.create_fake_data(products)
    return [data_manager, products, brand]
