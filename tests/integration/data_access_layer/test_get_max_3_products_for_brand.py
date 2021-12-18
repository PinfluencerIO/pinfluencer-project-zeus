from src.data_access_layer import to_list
from src.data_access_layer.read_data_access import load_max_3_products_for_brand
from tests.unit import InMemorySqliteDataManager, brand_generator, product_generator


def test_load_max_3_products_for_brand():
    data_manager = InMemorySqliteDataManager()
    brands = [brand_generator(1), brand_generator(2), brand_generator(3), brand_generator(4)]
    products = [product_generator(1, brands[0]),
                product_generator(2, brands[0]),
                product_generator(3, brands[0]),
                product_generator(4, brands[0]),
                product_generator(1, brands[1]),
                product_generator(2, brands[1]),
                product_generator(3, brands[1]),
                product_generator(1, brands[2])]
    data_manager.create_fake_data(brands)
    data_manager.create_fake_data(products)
    items = load_max_3_products_for_brand(data_manager=data_manager, type_=None)
    assert to_list([products[0],
                    products[1],
                    products[2],
                    products[4],
                    products[5],
                    products[6],
                    products[7]]) == to_list(items)
