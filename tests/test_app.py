from unittest import TestCase
from unittest.mock import Mock, MagicMock

from src.app import bootstrap
from src.crosscutting import JsonSnakeToCamelSerializer
from src.service import ServiceLocator
from src.types import Serializer
from tests import test_as_json


class TestRoutes(TestCase):

    def setUp(self) -> None:
        self.__mock_service_locator: ServiceLocator = Mock()
        self.__serializer: Serializer = JsonSnakeToCamelSerializer()
        self.__mock_service_locator.get_new_serializer = MagicMock(return_value=self.__serializer)

    def test_feed(self):
        response = bootstrap(event={"routeKey": "GET /feed"},
                             context={},
                             service_locator=self.__mock_service_locator)
        assert response == test_as_json(status_code=200)