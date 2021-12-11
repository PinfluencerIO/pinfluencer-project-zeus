import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product


def mock_load_products(data_manager):
    brand1 = Brand()
    brand1.id = str(uuid.UUID)

    product1 = Product()
    product1.id = str(uuid.uuid4())
    product1.brand = brand1
    product2 = Product()
    product2.id = str(uuid.uuid4())
    product2.brand = brand1

    return [product1, product2]

