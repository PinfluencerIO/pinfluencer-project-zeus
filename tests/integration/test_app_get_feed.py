import os
from unittest.mock import patch

from src.container import Container
from src.data_access_layer import to_list
from src.data_access_layer.brand import Brand
from src.pinfluencer_response import PinfluencerResponse
from src.routes import Routes
from tests.unit import brand_generator, product_generator, InMemorySqliteDataManager


def test_lambda_handler_get_feed():
    with patch.dict(os.environ, {'IN_MEMORY': 'True'}, clear=True):
        container = Container()
    products = pre_load_with_data(container.data_manager)
    routes = Routes(container)
    response: PinfluencerResponse = routes.routes["GET /feed"].do_process({})
    assert response.status_code == 200
    assert to_list(products) == response.body


def pre_load_with_data(data_manager: InMemorySqliteDataManager):
    brand1 = brand_generator(1)
    data_manager.create_fake_data([brand1])
    brand = data_manager.session.query(Brand).all()[0]
    products = [product_generator(1, brand), product_generator(2, brand)]
    data_manager.create_fake_data(products)
    return products
