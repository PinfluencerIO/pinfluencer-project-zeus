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
        self.__assert_brand_endpoint(expected_body="""{"allBrands": "some_all_brands_value"}""",
                                     brand_function="get_all",
                                     actual_body={"all_brands": "some_all_brands_value"},
                                     route_key="GET /brands")

    def test_get_brand_by_id(self):
        self.__assert_brand_endpoint(expected_body="""{"brandById": "some_brand_by_id_value"}""",
                                     brand_function="get_by_id",
                                     actual_body={"brand_by_id": "some_brand_by_id_value"},
                                     route_key="GET /brands/{brand_id}")

    def __assert_brand_endpoint(self,
                                expected_body: str,
                                actual_body: dict,
                                route_key: str,
                                brand_function: str):
        brand_controller: BrandController = Mock()
        setattr(brand_controller, brand_function, MagicMock(return_value=PinfluencerResponse(body=actual_body)))
        self.__mock_service_locator.get_new_brand_controller = MagicMock(return_value=brand_controller)
        response = bootstrap(event={"routeKey": route_key},
                             context={},
                             service_locator=self.__mock_service_locator)
        assert response == get_as_json(status_code=200, body=expected_body)