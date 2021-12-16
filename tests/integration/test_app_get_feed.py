import json
import os
from unittest.mock import patch

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product, product_from_dict
from tests.unit import brand_generator, product_generator

with patch.dict(os.environ, {'IN_MEMORY': 'True'}, clear=True):
    from src.app import lambda_handler
    import src.app


def test_lambda_handler_get_feed():
    product = pre_load_with_data()
    response = lambda_handler({"routeKey": "GET /feed"}, {})
    assert response['statusCode'] == 200
    dict = json.loads(response['body'])
    assert len(dict) == 1
    product_from_response_dict = product_from_dict(dict[0])
    assert product_from_response_dict.id == product.id
    assert product_from_response_dict.brand_id == product.brand_id
    assert product_from_response_dict.name == product.name


def pre_load_with_data():
    brand1 = brand_generator(1)
    src.app.container.data_manager.create_fake_data([brand1])
    brand = src.app.container.data_manager.session.query(Brand).all()[0]
    product1 = product_generator(1, brand)
    src.app.container.data_manager.create_fake_data([product1])
    product = src.app.container.data_manager.session.query(Product).all()[0]
    print(f'\nloaded {product}')
    return product
