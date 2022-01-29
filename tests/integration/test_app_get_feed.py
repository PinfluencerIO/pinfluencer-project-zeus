import os
from unittest.mock import patch

from src.container import Container
from src.routes import Routes


def test_lambda_handler_get_feed():
    with patch.dict(os.environ, {'IN_MEMORY': 'True'}, clear=True):
        container = Container()
    routes = Routes(container.data_manager, container.image_repository)
    response = routes.routes["GET /feed"]({})
    assert response.status_code == 200
