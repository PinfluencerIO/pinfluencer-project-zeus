import os
from unittest.mock import patch

from src.data_access_layer.data_access import DataManageFactory
from src.data_access_layer.repositories import S3ImageRepository
from src.routes import Routes


def test_lambda_handler_get_feed():
    with patch.dict(os.environ, {'IN_MEMORY': 'True'}, clear=True):
        routes = Routes(DataManageFactory.build(), S3ImageRepository())
    response = routes.routes["GET /feed"]({})
    assert response.status_code == 200
