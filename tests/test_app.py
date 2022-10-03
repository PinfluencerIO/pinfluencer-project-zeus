from os.path import exists
from typing import Union
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from callee import Any
from cfn_tools import load_yaml
from simple_injection import ServiceCollection

from src.app import bootstrap
from src.web import PinfluencerContext, PinfluencerResponse
from src.web.controllers import BrandController, CampaignController, InfluencerController
from src.web.hooks import CommonBeforeHooks, UserAfterHooks, BrandAfterHooks, UserBeforeHooks, \
    CampaignBeforeHooks, CampaignAfterHooks, BrandBeforeHooks, InfluencerAfterHooks, InfluencerBeforeHooks
from src.web.middleware import MiddlewarePipeline
from src.web.routing import Dispatcher
from src.web.sequences import NotImplementedSequenceBuilder, UpdateImageForCampaignSequenceBuilder, \
    UpdateCampaignSequenceBuilder, CreateCampaignSequenceBuilder, GetCampaignByIdSequenceBuilder, \
    GetCampaignsForBrandSequenceBuilder
from tests import get_as_json


class TestRoutes(TestCase):

    def setUp(self) -> None:
        self.__ioc: ServiceCollection = ServiceCollection()
        self.__mock_middleware_pipeline: MiddlewarePipeline = Mock()

    def test_server_error(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock(side_effect=Exception("some exception"))

        # act
        response = bootstrap(event={"routeKey": "GET /brands/{brand_id}"},
                             context={},
                             middleware=self.__mock_middleware_pipeline,
                             ioc=self.__ioc,
                             data_manager=Mock(),
                             cognito_auth_service=Mock())

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
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(BrandController).get_all,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response_collection,
                                         self.__ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images_collection,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories_collection
                                     ])

    def test_get_brand_by_id(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /brands/{brand_id}"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(BrandBeforeHooks).validate_uuid,
                                         self.__ioc.resolve(BrandController).get_by_id,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response,
                                         self.__ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories
                                     ])

    def test_get_all_influencers(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /influencers"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(InfluencerController).get_all,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response_collection,
                                         self.__ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images_collection,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories_collection
                                     ])

    def test_get_influencer_by_id(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /influencers/{influencer_id}"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(InfluencerBeforeHooks).validate_uuid,
                                         self.__ioc.resolve(InfluencerController).get_by_id,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response,
                                         self.__ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories
                                     ])

    def test_get_auth_brand(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /brands/me"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                         self.__ioc.resolve(BrandController).get,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response,
                                         self.__ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories
                                     ])

    def test_create_auth_brand(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /brands/me"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(CommonBeforeHooks).set_body,
                                         self.__ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                         self.__ioc.resolve(BrandBeforeHooks).validate_brand,
                                         self.__ioc.resolve(UserBeforeHooks).set_categories_and_values,
                                         self.__ioc.resolve(BrandController).create,
                                         self.__ioc.resolve(BrandAfterHooks).set_brand_claims,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response,
                                         self.__ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories
                                     ])

    def test_update_auth_brand(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "PATCH /brands/me"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(CommonBeforeHooks).set_body,
                                         self.__ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                         self.__ioc.resolve(BrandBeforeHooks).validate_brand,
                                         self.__ioc.resolve(UserBeforeHooks).set_categories_and_values,
                                         self.__ioc.resolve(BrandController).update_for_user,
                                         self.__ioc.resolve(BrandAfterHooks).set_brand_claims,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response,
                                         self.__ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories
                                     ])

    def test_create_or_replace_auth_brand_image(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /brands/me/images/{image_field}"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(CommonBeforeHooks).set_body,
                                         self.__ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                         self.__ioc.resolve(BrandBeforeHooks).validate_image_key,
                                         self.__ioc.resolve(BrandBeforeHooks).upload_image,
                                         self.__ioc.resolve(BrandController).update_image_field_for_user,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response,
                                         self.__ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories
                                     ])

    def test_get_auth_influencer(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /influencers/me"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                         self.__ioc.resolve(InfluencerController).get,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response,
                                         self.__ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories
                                     ])

    def test_create_auth_influencer(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /influencers/me"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(CommonBeforeHooks).set_body,
                                         self.__ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                         self.__ioc.resolve(InfluencerBeforeHooks).validate_influencer,
                                         self.__ioc.resolve(UserBeforeHooks).set_categories_and_values,
                                         self.__ioc.resolve(InfluencerController).create,
                                         self.__ioc.resolve(InfluencerAfterHooks).set_influencer_claims,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response,
                                         self.__ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories
                                     ])

    def test_update_auth_influencer_image(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /influencers/me/images/{image_field}"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(CommonBeforeHooks).set_body,
                                         self.__ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                         self.__ioc.resolve(InfluencerBeforeHooks).validate_image_key,
                                         self.__ioc.resolve(InfluencerBeforeHooks).upload_image,
                                         self.__ioc.resolve(InfluencerController).update_image_field_for_user,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response,
                                         self.__ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories
                                     ])

    def test_update_auth_influencer(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "PATCH /influencers/me"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     middleware=[
                                         self.__ioc.resolve(CommonBeforeHooks).set_body,
                                         self.__ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                         self.__ioc.resolve(InfluencerBeforeHooks).validate_influencer,
                                         self.__ioc.resolve(UserBeforeHooks).set_categories_and_values,
                                         self.__ioc.resolve(InfluencerController).update_for_user,
                                         self.__ioc.resolve(InfluencerAfterHooks).set_influencer_claims,
                                         self.__ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response,
                                         self.__ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images,
                                         self.__ioc.resolve(UserAfterHooks).format_values_and_categories
                                     ])

    def test_create_auth_brand_campaign(self):  # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /brands/me/campaigns"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     sequence=self.__ioc.resolve(CreateCampaignSequenceBuilder))

    def test_get_campaign_by_id(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /campaigns/{campaign_id}"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     sequence=self.__ioc.resolve(GetCampaignByIdSequenceBuilder))

    def test_get_auth_brand_campaigns(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "GET /brands/me/campaigns"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     sequence=self.__ioc.resolve(GetCampaignsForBrandSequenceBuilder))

    def test_update_brand_auth_campaign_by_id(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "PATCH /brands/me/campaigns/{campaign_id}"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     sequence=self.__ioc.resolve(UpdateCampaignSequenceBuilder))

    def test_delete_brand_auth_campaign_by_id(self):
        self.__assert_not_implemented(route="DELETE /brands/me/campaigns/{campaign_id}")

    def test_create_campaign_product_image(self):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()

        # act
        bootstrap(event={"routeKey": "POST /brands/me/campaigns/{campaign_id}/images/{image_field}"},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        self.__mock_middleware_pipeline \
            .execute_middleware \
            .assert_called_once_with(context=Any(),
                                     sequence=self.__ioc.resolve(UpdateImageForCampaignSequenceBuilder))

    def test_get_notification_by_id(self):
        self.__assert_not_implemented(route="GET /notifications/{notification_id}")

    def test_get_collaboration_by_id(self):
        self.__assert_not_implemented(route="GET /collaborations/{collaboration_id}")

    def test_create_collaboration(self):
        self.__assert_not_implemented(route="POST /influencers/me/collaborations")

    def test_update_collaboration(self):
        self.__assert_not_implemented(route="PATCH /influencers/me/collaborations/{collaboration_id}")

    def test_get_collaborations_for_brand(self):
        self.__assert_not_implemented(route="GET /brands/me/collaborations")

    def test_get_collaborations_for_influencer(self):
        self.__assert_not_implemented(route="GET /influencers/me/collaborations")

    def test_get_notifications_for_sender(self):
        self.__assert_not_implemented(route="GET /senders/me/notifications")

    def test_get_notifications_for_receiver(self):
        self.__assert_not_implemented(route="GET /receivers/me/notifications")

    def test_create_notification_for_user(self):
        self.__assert_not_implemented(route="POST /users/me/notifications")

    def test_update_notification_for_user(self):
        self.__assert_not_implemented(route="PATCH /users/me/notifications")

    def test_template_matches_routes(self):
        template_file_path = f"./../template.yaml"
        if not exists(template_file_path):
            template_file_path = f"./template.yaml"
        with open(template_file_path) as file:
            yaml_str = file.read()
            data = load_yaml(yaml_str)
            paths = sorted([f"{event[1]['Properties']['Method'].upper()} {event[1]['Properties']['Path']}" for event in
                            data["Resources"]["PinfluencerFunction"]["Properties"]["Events"].items()])
            route_paths = sorted([*Dispatcher(brand_ctr=Mock(),
                                              campaign_ctr=Mock(),
                                              hooks_facade=Mock(),
                                              influencer_ctr=Mock(),
                                              update_image_for_campaign_sequence=Mock(),
                                              not_implemented_sequence_builder=Mock(),
                                              update_campaign_sequence_builder=Mock()).dispatch_route_to_ctr])
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
        setattr(self.__ioc, service_name, MagicMock(return_value=service))

        # act
        response = bootstrap(event={"routeKey": route_key},
                             context={},
                             middleware=self.__mock_middleware_pipeline,
                             ioc=self.__ioc,
                             data_manager=Mock(),
                             cognito_auth_service=Mock())

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
                             middleware=self.__mock_middleware_pipeline,
                             ioc=self.__ioc,
                             data_manager=Mock(),
                             cognito_auth_service=Mock())

        # assert
        assert response == get_as_json(status_code=expected_status_code, body=expected_body)

    def __assert_not_implemented(self, route: str):
        # arrange
        self.__mock_middleware_pipeline.execute_middleware = MagicMock()
        context = PinfluencerContext(response=PinfluencerResponse())

        # act
        bootstrap(event={"routeKey": route},
                  context={},
                  middleware=self.__mock_middleware_pipeline,
                  ioc=self.__ioc,
                  data_manager=Mock(),
                  cognito_auth_service=Mock())

        # assert
        with self.subTest(msg="pipeline executes once"):
            self.__mock_middleware_pipeline \
                .execute_middleware \
                .assert_called_once_with(context=Any(),
                                         sequence=self.__ioc.resolve(NotImplementedSequenceBuilder))
