import os
from typing import Union
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from cfn_tools import load_yaml

from src.app import bootstrap
from src.crosscutting import JsonSnakeToCamelSerializer
from src.service import ServiceLocator
from src.types import Serializer
from src.web import PinfluencerResponse
from src.web.controllers import BrandController
from src.web.routing import Dispatcher
from tests import get_as_json


class TestRoutes(TestCase):

    def setUp(self) -> None:
        self.__mock_service_locator: ServiceLocator = Mock()
        self.__serializer: Serializer = JsonSnakeToCamelSerializer()
        self.__mock_service_locator.get_new_serializer = MagicMock(return_value=self.__serializer)

    def test_server_error(self):
        brand_controller: BrandController = Mock()
        setattr(brand_controller, 'get_by_id', MagicMock(side_effect=Exception("some exception is thrown")))
        self.__mock_service_locator.get_new_brand_controller = MagicMock(return_value=brand_controller)
        response = bootstrap(event={"routeKey": "GET /brands/{brand_id}"},
                             context={},
                             service_locator=self.__mock_service_locator)
        assert response == get_as_json(status_code=500,
                                       body="""{"message": "unexpected server error, please try later :("}""")

    def test_route_that_does_not_exist(self):
        self.__assert_non_service_layer_route(route_key="GET /random",
                                              expected_body="""{"message": "route: GET /random not found"}""",
                                              expected_status_code=404)

    def test_feed(self):
        self.__assert_non_service_layer_route(route_key="GET /feed",
                                              expected_body="""{"message": "GET /feed is not implemented"}""",
                                              expected_status_code=405)

    def test_get_all_brands(self):
        self.__assert_service_endpoint_200(expected_body="""{"allBrands": "some_all_brands_value"}""",
                                           service_function="get_all",
                                           actual_body={"all_brands": "some_all_brands_value"},
                                           route_key="GET /brands",
                                           service_name="get_new_brand_controller")

    def test_get_all_empty_list(self):
        self.__assert_service_endpoint_200(expected_body="""[]""",
                                           service_function="get_all",
                                           actual_body=[],
                                           route_key="GET /brands",
                                           service_name="get_new_brand_controller")

    def test_get_brand_by_id(self):
        self.__assert_service_endpoint_200(expected_body="""{"brandById": "some_brand_by_id_value"}""",
                                           service_function="get_by_id",
                                           actual_body={"brand_by_id": "some_brand_by_id_value"},
                                           route_key="GET /brands/{brand_id}",
                                           service_name="get_new_brand_controller")

    def test_get_all_influencers(self):
        self.__assert_service_endpoint_200(expected_body="""{"getAllInfluencers": "some_influencer_value"}""",
                                           service_function="get_all",
                                           actual_body={"get_all_influencers": "some_influencer_value"},
                                           route_key="GET /influencers",
                                           service_name="get_new_influencer_controller")

    def test_get_influencer_by_id(self):
        self.__assert_service_endpoint_200(expected_body="""{"getInfluencerById": "some_influencer_by_id_value"}""",
                                           service_function="get_by_id",
                                           actual_body={"get_influencer_by_id": "some_influencer_by_id_value"},
                                           route_key="GET /influencers/{influencer_id}",
                                           service_name="get_new_influencer_controller")

    def test_get_auth_brand(self):
        self.__assert_service_endpoint_200(expected_body="""{"getBrandMe": "some_brand_auth_value"}""",
                                           service_function="get",
                                           actual_body={"get_brand_me": "some_brand_auth_value"},
                                           route_key="GET /brands/me",
                                           service_name="get_new_brand_controller")

    def test_create_auth_brand(self):
        self.__assert_service_endpoint_200(expected_body="""{"createBrandMe": "some_brand_auth_value"}""",
                                           service_function="create",
                                           actual_body={"create_brand_me": "some_brand_auth_value"},
                                           route_key="POST /brands/me",
                                           service_name="get_new_brand_controller")

    def test_update_auth_brand(self):
        self.__assert_service_endpoint_200(expected_body="""{"updateBrandMe": "some_brand_auth_value"}""",
                                           service_function="update",
                                           actual_body={"update_brand_me": "some_brand_auth_value"},
                                           route_key="PUT /brands/me",
                                           service_name="get_new_brand_controller")

    def test_create_or_replace_auth_brand_header_image(self):
        self.__assert_service_endpoint_200(expected_body="""{"updateBrandMeHeaderImage": "some_brand_auth_value"}""",
                                           service_function="update_header_image",
                                           actual_body={"update_brand_me_header_image": "some_brand_auth_value"},
                                           route_key="POST /brands/me/header-image",
                                           service_name="get_new_brand_controller")

    def test_create_or_replace_auth_brand_logo(self):
        self.__assert_service_endpoint_200(expected_body="""{"updateBrandMeLogo": "some_brand_auth_value"}""",
                                           service_function="update_logo",
                                           actual_body={"update_brand_me_logo": "some_brand_auth_value"},
                                           route_key="POST /brands/me/logo",
                                           service_name="get_new_brand_controller")

    def test_get_auth_influencer(self):
        self.__assert_service_endpoint_200(expected_body="""{"getAuthInfluencer": "some_influencer_value"}""",
                                           service_function="get",
                                           actual_body={"get_auth_influencer": "some_influencer_value"},
                                           route_key="GET /influencers/me",
                                           service_name="get_new_influencer_controller")

    def test_create_auth_influencer(self):
        self.__assert_service_endpoint_200(expected_body="""{"createAuthInfluencer": "some_influencer_value"}""",
                                           service_function="create",
                                           actual_body={"create_auth_influencer": "some_influencer_value"},
                                           route_key="POST /influencers/me",
                                           service_name="get_new_influencer_controller")

    def test_update_auth_influencer(self):
        self.__assert_non_service_layer_route(
            expected_body="""{"message": "POST /influencers/me/image is not implemented"}""",
            expected_status_code=405,
            route_key="POST /influencers/me/image")

    def test_get_auth_campaigns(self):
        self.__assert_non_service_layer_route(
            expected_body="""{"message": "GET /campaigns/me is not implemented"}""",
            expected_status_code=405,
            route_key="GET /campaigns/me")

    def test_delete_auth_campaign_by_id(self):
        self.__assert_non_service_layer_route(
            expected_body="""{"message": "DELETE /campaigns/me/{campaign_id} is not implemented"}""",
            expected_status_code=405,
            route_key="DELETE /campaigns/me/{campaign_id}")

    def test_get_auth_campaign_by_id(self):
        self.__assert_non_service_layer_route(
            expected_body="""{"message": "GET /campaigns/me/{campaign_id} is not implemented"}""",
            expected_status_code=405,
            route_key="GET /campaigns/me/{campaign_id}")

    def test_update_auth_campaign_by_id(self):
        self.__assert_non_service_layer_route(
            expected_body="""{"message": "PUT /campaigns/me/{campaign_id} is not implemented"}""",
            expected_status_code=405,
            route_key="PUT /campaigns/me/{campaign_id}")

    def test_create_auth_campaign(self):
        self.__assert_non_service_layer_route(
            expected_body="""{"message": "POST /campaigns/me is not implemented"}""",
            expected_status_code=405,
            route_key="POST /campaigns/me")

    def test_template_matches_routes(self):
        template_file_path = f"./../template.yaml"
        if "REMOTE_BUILD" in os.environ:
            template_file_path = f"./template.yaml"
        with open(template_file_path) as file:
            yaml_str = file.read()
            data = load_yaml(yaml_str)
            paths = sorted([f"{event[1]['Properties']['Method'].upper()} {event[1]['Properties']['Path']}" for event in data["Resources"]["PinfluencerFunction"]["Properties"]["Events"].items()])
            route_paths = sorted([*Dispatcher(service_locator=self.__mock_service_locator).dispatch_route_to_ctr])
            assert paths == route_paths

    def __assert_service_endpoint_200(self,
                                      expected_body: str,
                                      actual_body: Union[dict, list],
                                      route_key: str,
                                      service_function: str,
                                      service_name: str):
        service = Mock()
        setattr(service, service_function, MagicMock(return_value=PinfluencerResponse(body=actual_body)))
        setattr(self.__mock_service_locator, service_name, MagicMock(return_value=service))
        response = bootstrap(event={"routeKey": route_key},
                             context={},
                             service_locator=self.__mock_service_locator)
        assert response == get_as_json(status_code=200, body=expected_body)

    def __assert_non_service_layer_route(self,
                                         route_key: str,
                                         expected_body: str,
                                         expected_status_code: int):
        """
        any routes that do not access services from IOC container, like not found or not implemented routes
        """
        response = bootstrap(event={"routeKey": route_key},
                             context={},
                             service_locator=self.__mock_service_locator)
        assert response == get_as_json(status_code=expected_status_code, body=expected_body)
