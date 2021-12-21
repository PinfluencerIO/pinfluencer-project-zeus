from src.data_access_layer import to_list
from src.data_access_layer.read_data_access import load_max_3_products_for_brand
from tests import InMemorySqliteDataManager, brand_generator, product_generator


def test_load_max_3_products_for_brand_when_many_products_are_available_for_many_brands():
    brands = [brand_generator(1), brand_generator(2)]
    products = [product_generator(1, brands[0]),
                product_generator(2, brands[0]),
                product_generator(2, brands[1]),
                product_generator(2, brands[1]),
                product_generator(2, brands[1])]
    data_manager = setup_database(brands, products)
    assert_test(data_manager, products)


def test_load_max_3_products_for_brand_when_less_than_3_products_are_available():
    brands = [brand_generator(1)]
    products = [product_generator(1, brands[0]),
                product_generator(2, brands[0])]
    data_manager = setup_database(brands, products)
    assert_test(data_manager, products)


def test_load_max_3_products_for_brand_when_more_than_3_products_are_available():
    brands = [brand_generator(1)]
    products = [product_generator(1, brands[0]),
                product_generator(2, brands[0]),
                product_generator(3, brands[0]),
                product_generator(4, brands[0])]
    data_manager = setup_database(brands, products)
    assert_test(data_manager, products[:3])


def test_load_max_3_products_for_brand_when_no_products_are_available():
    brands = [brand_generator(1)]
    data_manager = setup_database(brands, [])
    assert_test(data_manager, [])


def test_load_max_3_products_for_brand_when_brands_are_available():
    data_manager = setup_database([], [])
    assert_test(data_manager, [])


def setup_database(brands, products):
    data_manager = InMemorySqliteDataManager()
    data_manager.create_fake_data(brands)
    data_manager.create_fake_data(products)
    return data_manager


def assert_test(data_manager, expected):
    items = load_max_3_products_for_brand(data_manager=data_manager, type_=None)
    assert to_list(expected) == to_list(items)
