import os
from typing import Union
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from callee import Any, Captor
from cfn_tools import load_yaml

from src.app import bootstrap
from src.crosscutting import JsonSnakeToCamelSerializer
from src.types import Serializer
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.controllers import BrandController, InfluencerController, CampaignController
from src.web.hooks import HooksFacade, CommonBeforeHooks, UserAfterHooks, BrandAfterHooks, UserBeforeHooks, \
    BrandBeforeHooks, InfluencerAfterHooks, InfluencerBeforeHooks, CampaignBeforeHooks, CampaignAfterHooks
from src.web.ioc import ServiceLocator
from src.web.middleware import MiddlewarePipeline
from src.web.routing import Dispatcher
from tests import get_as_json


class TestRoutes(TestCase):

    def setUp(self) -> None:
        # controllers
        self.__mock_service_locator: ServiceLocator = Mock()
        self.__mock_brand_controller: BrandController = Mock()
        self.__mock_service_locator.get_new_brand_controller = MagicMock(return_value=self.__mock_brand_controller)
        self.__mock_campaign_controller: CampaignController = Mock()
        self.__mock_service_locator.get_new_campaign_controller = MagicMock(
            return_value=self.__mock_campaign_controller)
        self.__mock_influencer_controller: InfluencerController = Mock()
        self.__mock_service_locator.get_new_influencer_controller = MagicMock(
            return_value=self.__mock_influencer_controller)

        # hooks
        self.__hooks_facade: HooksFacade = Mock()
        self.__common_hooks: CommonBeforeHooks = Mock()
        self.__user_after_hooks: UserAfterHooks = Mock()
        self.__brand_after_hooks: BrandAfterHooks = Mock()
        self.__user_before_hooks: UserBeforeHooks = Mock()
        self.__brand_before_hooks: BrandBeforeHooks = Mock()
        self.__influencer_after_hooks: InfluencerAfterHooks = Mock()
        self.__influencer_before_hooks: InfluencerBeforeHooks = Mock()
        self.__campaign_before_hooks: CampaignBeforeHooks = Mock()
        self.__campaign_after_hooks: CampaignAfterHooks = Mock()
        self.__hooks_facade.get_campaign_after_hooks = MagicMock(return_value=self.__campaign_after_hooks)
        self.__hooks_facade.get_campaign_before_hooks = MagicMock(return_value=self.__campaign_before_hooks)
        self.__hooks_facade.get_before_common_hooks = MagicMock(return_value=self.__common_hooks)
        self.__hooks_facade.get_user_after_hooks = MagicMock(return_value=self.__user_after_hooks)
        self.__hooks_facade.get_brand_after_hooks = MagicMock(return_value=self.__brand_after_hooks)
        self.__hooks_facade.get_user_before_hooks = MagicMock(return_value=self.__user_before_hooks)
        self.__hooks_facade.get_brand_before_hooks = MagicMock(return_value=self.__brand_before_hooks)
        self.__hooks_facade.get_influencer_after_hooks = MagicMock(return_value=self.__influencer_after_hooks)
        self.__hooks_facade.get_influencer_before_hooks = MagicMock(return_value=self.__influencer_before_hooks)
        self.__mock_service_locator.get_new_hooks_facade = MagicMock(return_value=self.__hooks_facade)

        # crosscutting
        self.__serializer: Serializer = JsonSnakeToCamelSerializer()
        self.__mock_service_locator.get_new_serializer = MagicMock(return_value=self.__serializer)

        # middleware
        self.__mock_middleware_pipeline: MiddlewarePipeline = Mock()
        self.__mock_service_locator.get_new_middlware_pipeline = MagicMock(return_value=self.__mock_middleware_pipeline)

    def test_server_error(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock(side_effect=Exception("some exception"))

        # act
        response = bootstrap(event={"routeKey": "GET /brands/{brand_id}"},
                             context={},
                             service_locator=self.__mock_service_locator)

        # assert
        assert response == get_as_json(status_code=500,
                                       body="""{"message": "unexpected server error, please try later :("}""")

    def test_route_that_does_not_exist(self):
        self.__assert_non_service_layer_route(route_key="GET /random",
                                              expected_body="""{"message": "route: GET /random not found"}""",
                                              expected_status_code=404)

    def test_feed(self):
        self.__assert_not_implemented(route="GET /feed")

    def test_get_all_brands(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /brands"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__mock_brand_controller.get_all,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response_collection,
                                         self.__brand_after_hooks.tag_bucket_url_to_images_collection,
                                         self.__user_after_hooks.format_values_and_categories_collection
                                     ])

    def test_get_brand_by_id(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /brands/{brand_id}"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__brand_before_hooks.validate_uuid,
                                         self.__mock_brand_controller.get_by_id,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__brand_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_get_all_influencers(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /influencers"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__mock_influencer_controller.get_all,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response_collection,
                                         self.__influencer_after_hooks.tag_bucket_url_to_images_collection,
                                         self.__user_after_hooks.format_values_and_categories_collection
                                     ])

    def test_get_influencer_by_id(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /influencers/{influencer_id}"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__influencer_before_hooks.validate_uuid,
                                         self.__mock_influencer_controller.get_by_id,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__influencer_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_get_auth_brand(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /brands/me"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__mock_brand_controller.get,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__brand_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_create_auth_brand(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /brands/me"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__common_hooks.set_body,
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__brand_before_hooks.validate_brand,
                                         self.__mock_brand_controller.create,
                                         self.__brand_after_hooks.set_brand_claims,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__brand_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_update_auth_brand(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "PUT /brands/me"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__common_hooks.set_body,
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__brand_before_hooks.validate_brand,
                                         self.__mock_brand_controller.update,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__brand_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_create_or_replace_auth_brand_header_image(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /brands/me/header-image"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__common_hooks.set_body,
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__mock_brand_controller.update_header_image,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__brand_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_create_or_replace_auth_brand_logo(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /brands/me/logo"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__common_hooks.set_body,
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__mock_brand_controller.update_logo,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__brand_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_get_auth_influencer(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /influencers/me"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__mock_influencer_controller.get,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__influencer_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_create_auth_influencer(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /influencers/me"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__common_hooks.set_body,
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__influencer_before_hooks.validate_influencer,
                                         self.__mock_influencer_controller.create,
                                         self.__influencer_after_hooks.set_influencer_claims,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__influencer_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_update_auth_influencer_image(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /influencers/me/image"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__common_hooks.set_body,
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__mock_influencer_controller.update_profile_image,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__influencer_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_update_auth_influencer(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "PUT /influencers/me"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__common_hooks.set_body,
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__influencer_before_hooks.validate_influencer,
                                         self.__mock_influencer_controller.update,
                                         self.__user_after_hooks.tag_auth_user_claims_to_response,
                                         self.__influencer_after_hooks.tag_bucket_url_to_images,
                                         self.__user_after_hooks.format_values_and_categories
                                     ])

    def test_create_auth_brand_campaign(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /brands/me/campaigns"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__common_hooks.set_body,
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__campaign_before_hooks.validate_campaign,
                                         self.__mock_campaign_controller.create,
                                         self.__campaign_after_hooks.format_values_and_categories,
                                         self.__campaign_after_hooks.tag_bucket_url_to_images
                                     ])

    def test_get_campaign_by_id(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /campaigns/{campaign_id}"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__campaign_before_hooks.validate_id,
                                         self.__mock_campaign_controller.get_by_id,
                                         self.__campaign_after_hooks.format_values_and_categories,
                                         self.__campaign_after_hooks.tag_bucket_url_to_images
                                     ])

    def test_get_auth_brand_campaigns(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /brands/me/campaigns"},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__user_before_hooks.set_auth_user_id,
                                         self.__mock_campaign_controller.get_for_brand,
                                         self.__campaign_after_hooks.format_values_and_categories_collection,
                                         self.__campaign_after_hooks.tag_bucket_url_to_images_collection
                                     ])

    def test_update_brand_auth_campaign_by_id(self):
        self.__assert_not_implemented(route="PUT /brands/me/campaigns/{campaign_id}")

    def test_delete_brand_auth_campaign_by_id(self):
        self.__assert_not_implemented(route="DELETE /brands/me/campaigns/{campaign_id}")

    def test_create_campaign_product_image1(self):
        self.__assert_not_implemented(route="POST /campaigns/{campaign_id}/product-image1")

    def test_create_campaign_product_image2(self):
        self.__assert_not_implemented(route="POST /campaigns/{campaign_id}/product-image2")

    def test_create_campaign_product_image3(self):
        self.__assert_not_implemented(route="POST /campaigns/{campaign_id}/product-image3")

    def test_template_matches_routes(self):
        template_file_path = f"./../template.yaml"
        if "REMOTE_BUILD" in os.environ:
            template_file_path = f"./template.yaml"
        with open(template_file_path) as file:
            yaml_str = file.read()
            data = load_yaml(yaml_str)
            paths = sorted([f"{event[1]['Properties']['Method'].upper()} {event[1]['Properties']['Path']}" for event in
                            data["Resources"]["PinfluencerFunction"]["Properties"]["Events"].items()])
            route_paths = sorted([*Dispatcher(service_locator=self.__mock_service_locator).dispatch_route_to_ctr])
            assert paths == route_paths

    def __assert_service_endpoint_200(self,
                                      expected_body: str,
                                      actual_body: Union[dict, list],
                                      route_key: str,
                                      service_function: str,
                                      service_name: str):
        # arrange
        service = Mock()
        setattr(service, service_function,
                MagicMock(side_effect=lambda x: self.__service_side_effect(context=x, actual_body=actual_body)))
        setattr(self.__mock_service_locator, service_name, MagicMock(return_value=service))

        # act
        response = bootstrap(event={"routeKey": route_key},
                             context={},
                             service_locator=self.__mock_service_locator)

        # assert
        assert response == get_as_json(status_code=200, body=expected_body)

    def __service_side_effect(self, context: PinfluencerContext, actual_body: dict):
        context.response.body = actual_body

    def __assert_non_service_layer_route(self,
                                         route_key: str,
                                         expected_body: str,
                                         expected_status_code: int):
        """
        any routes that do not access services from IOC container, like not found or not implemented routes
        """

        # arrange/act
        response = bootstrap(event={"routeKey": route_key},
                             context={},
                             service_locator=self.__mock_service_locator)

        # assert
        assert response == get_as_json(status_code=expected_status_code, body=expected_body)

    def __assert_not_implemented(self, route: str):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()
        context = PinfluencerContext(response=PinfluencerResponse())

        # act
        bootstrap(event={"routeKey": route},
                  context={},
                  service_locator=self.__mock_service_locator)

        # assert
        captor = Captor()
        self.__mock_middleware_pipeline.execute_middleware.assert_called_once_with(context=Any(),
                                                                                   middleware=captor)
        captor.arg[0](context)
        assert context.response.status_code == 405
