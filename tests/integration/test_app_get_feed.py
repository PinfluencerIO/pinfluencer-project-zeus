import os
from unittest.mock import patch

from src.container import Container
from src.data_access_layer import to_list
from src.routes import Routes


def test_lambda_handler_get_feed():
    with patch.dict(os.environ, {'IN_MEMORY': 'True'}, clear=True):
        container = Container()
    routes = Routes(container)
    response = routes.routes["GET /feed"].do_process({})
    assert response.status_code == 200
