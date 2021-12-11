from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product


def mock_load_max_3_products_for_brand(brand_id, data_manager):
    brand = Brand()
    brand.id = brand_id
    product1_1 = Product()
    product1_1.brand = brand
    product2_1 = Product()
    product2_1.brand = brand
    product3_1 = Product()
    product3_1.brand = brand

    return [product1_1, product2_1, product3_1]
