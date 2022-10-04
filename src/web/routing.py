from collections import OrderedDict

from src import ServiceLocator
from src.web import Route
from src.web.controllers import CampaignController, BrandController, InfluencerController
from src.web.hooks import HooksFacade
from src.web.sequences import UpdateCampaignSequenceBuilder, UpdateImageForCampaignSequenceBuilder, \
    NotImplementedSequenceBuilder, CreateCampaignSequenceBuilder, GetCampaignByIdSequenceBuilder, \
    GetCampaignsForBrandSequenceBuilder, UpdateInfluencerImageSequenceBuilder, UpdateInfluencerSequenceBuilder, \
    CreateInfluencerSequenceBuilder, GetAuthInfluencerSequenceBuilder, GetInfluencerByIdSequenceBuilder, \
    GetAllInfluencersSequenceBuilder


class Dispatcher:
    def __init__(self, campaign_ctr: CampaignController,
                 brand_ctr: BrandController,
                 influencer_ctr: InfluencerController,
                 hooks_facade: HooksFacade,
                 service_locator: ServiceLocator):
        self.__service_locator = service_locator
        self.__campaign_ctr = campaign_ctr
        self.__brand_ctr = brand_ctr
        self.__influencer_ctr = influencer_ctr
        self.__hooks_facade = hooks_facade

    @property
    def dispatch_route_to_ctr(self) -> dict[dict[str, Route]]:
        feed = OrderedDict(
            {
                'GET /feed':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))
            }
        )

        users = OrderedDict(
            {
                'GET /brands': self.get_all_brands(),

                'GET /influencers':
                    Route(sequence_builder=self.__service_locator.locate(GetAllInfluencersSequenceBuilder)),

                'GET /brands/{brand_id}': self.get_brand_by_id(),

                'GET /influencers/{influencer_id}':
                    Route(sequence_builder=self.__service_locator.locate(GetInfluencerByIdSequenceBuilder)),

                # authenticated brand endpoints
                'GET /brands/me': self.get_auth_brand(),

                'POST /brands/me': self.create_brand(),

                'PATCH /brands/me': self.update_brand(),

                'POST /brands/me/images/{image_field}': self.update_brand_image(),

                # authenticated influencer endpoints
                'GET /influencers/me':
                    Route(sequence_builder=self.__service_locator.locate(GetAuthInfluencerSequenceBuilder)),

                'POST /influencers/me':
                    Route(self.__service_locator.locate(CreateInfluencerSequenceBuilder)),

                'PATCH /influencers/me':
                    Route(self.__service_locator.locate(UpdateInfluencerSequenceBuilder)),

                'POST /influencers/me/images/{image_field}':
                    Route(self.__service_locator.locate(UpdateInfluencerImageSequenceBuilder)),
            }
        )

        campaigns = OrderedDict(
            {
                'GET /brands/me/campaigns':
                    Route(sequence_builder=self.__service_locator.locate(GetCampaignsForBrandSequenceBuilder)),

                'DELETE /brands/me/campaigns/{campaign_id}':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'GET /campaigns/{campaign_id}':
                    Route(sequence_builder=self.__service_locator.locate(GetCampaignByIdSequenceBuilder)),

                'POST /brands/me/campaigns':
                    Route(sequence_builder=self.__service_locator.locate(CreateCampaignSequenceBuilder)),

                'PATCH /brands/me/campaigns/{campaign_id}':
                    Route(sequence_builder=self.__service_locator.locate(UpdateCampaignSequenceBuilder)),

                'POST /brands/me/campaigns/{campaign_id}/images/{image_field}':
                    Route(sequence_builder=self.__service_locator.locate(UpdateImageForCampaignSequenceBuilder))
            }
        )

        collaborations = OrderedDict(
            {
                'GET /collaborations/{collaboration_id}':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'POST /influencers/me/collaborations':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'PATCH /influencers/me/collaborations/{collaboration_id}':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'GET /influencers/me/collaborations':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'GET /brands/me/collaborations':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))
            }
        )

        notifications = OrderedDict(
            {
                'GET /notifications/{notification_id}':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'POST /users/me/notifications':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'PATCH /users/me/notifications':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'GET /receivers/me/notifications':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'GET /senders/me/notifications':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))
            }
        )

        routes = {}
        routes.update(feed)
        routes.update(users)
        routes.update(campaigns)
        routes.update(collaborations)
        routes.update(notifications)
        return routes

    def update_brand_image(self):
        '''
            TODO:
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_brand_before_hooks().validate_image_key,
                self.__hooks_facade.get_brand_before_hooks().upload_image
                self.__brand_ctr.update_image_field_for_user,
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
        '''
        return Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))

    def update_brand(self):
        '''
            TODO:
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_brand_before_hooks().validate_brand,
                self.__hooks_facade.get_user_before_hooks().set_categories_and_values
                self.__brand_ctr.update_for_user,
                self.__hooks_facade.get_brand_after_hooks().set_brand_claims,
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
        '''
        return Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))

    def create_brand(self):
        '''
            TODO:
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_brand_before_hooks().validate_brand,
                self.__hooks_facade.get_user_before_hooks().set_categories_and_values
                self.__brand_ctr.create,
                self.__hooks_facade.get_brand_after_hooks().set_brand_claims,
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
        '''
        return Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))

    def get_auth_brand(self):
        '''
            TODO:
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id
                self.__brand_ctr.get,
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
        '''
        return Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))

    def get_brand_by_id(self):
        '''
            TODO:
                self.__hooks_facade.get_brand_before_hooks().validate_uuid
                self.__brand_ctr.get_by_id,
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
        '''
        return Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))

    def get_all_brands(self):
        '''
            TODO:
                self.__brand_ctr.get_all,
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response_collection,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images_collection,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories_collection
        '''
        return Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))
