from unittest import TestCase
from unittest.mock import Mock, MagicMock

from src.app import bootstrap
from src.crosscutting import JsonSnakeToCamelSerializer
from src.service import ServiceLocator
from src.types import Serializer
from src.web import PinfluencerResponse
from src.web.controllers import BrandController
from tests import get_as_json


class TestRoutes(TestCase):

    def setUp(self) -> None:
        self.__mock_service_locator: ServiceLocator = Mock()
        self.__serializer: Serializer = JsonSnakeToCamelSerializer()
        self.__mock_service_locator.get_new_serializer = MagicMock(return_value=self.__serializer)

    def test_feed(self):
        response = bootstrap(event={"routeKey": "GET /feed"},
                             context={},
                             service_locator=self.__mock_service_locator)
        assert response == get_as_json(status_code=200)

    def test_get_all_brands(self):
        brand_controller: BrandController = Mock()
        brand_controller.get_all = MagicMock(return_value=PinfluencerResponse(body={"some_key": "some_value"}))
        self.__mock_service_locator.get_new_brand_controller = MagicMock(return_value=brand_controller)
        response = bootstrap(event={"routeKey": "GET /brands"},
                             context={},
                             service_locator=self.__mock_service_locator)
        assert response == get_as_json(status_code=200, body="""{"someKey": "some_value"}""")