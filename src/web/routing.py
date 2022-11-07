from collections import OrderedDict

from src import ServiceLocator
from src.web import Route
from src.web.sequences import UpdateCampaignSequenceBuilder, UpdateImageForCampaignSequenceBuilder, \
    NotImplementedSequenceBuilder, CreateCampaignSequenceBuilder, GetCampaignByIdSequenceBuilder, \
    GetCampaignsForBrandSequenceBuilder, UpdateInfluencerImageSequenceBuilder, UpdateInfluencerSequenceBuilder, \
    CreateInfluencerSequenceBuilder, GetAuthInfluencerSequenceBuilder, GetInfluencerByIdSequenceBuilder, \
    GetAllInfluencersSequenceBuilder, UpdateBrandImageSequenceBuilder, UpdateBrandSequenceBuilder, \
    CreateBrandSequenceBuilder, GetAuthBrandSequenceBuilder, GetBrandByIdSequenceBuilder, GetAllBrandsSequenceBuilder, \
    CreateNotificationSequenceBuilder, GetNotificationByIdSequenceBuilder, CreateAudienceAgeSequenceBuilder, \
    GetAudienceAgeSequenceBuilder


class Dispatcher:
    def __init__(self, service_locator: ServiceLocator):
        self.__service_locator = service_locator

    @property
    def dispatch_route_to_ctr(self) -> dict[dict[str, Route]]:
        feed_routes = OrderedDict(
            {
                'GET /feed':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))
            }
        )

        user_routes = OrderedDict(
            {
                'GET /brands':
                    Route(sequence_builder=self.__service_locator.locate(GetAllBrandsSequenceBuilder)),

                'GET /influencers':
                    Route(sequence_builder=self.__service_locator.locate(GetAllInfluencersSequenceBuilder)),

                'GET /brands/{brand_id}':
                    Route(sequence_builder=self.__service_locator.locate(GetBrandByIdSequenceBuilder)),

                'GET /influencers/{influencer_id}':
                    Route(sequence_builder=self.__service_locator.locate(GetInfluencerByIdSequenceBuilder)),

                # authenticated brand endpoints
                'GET /brands/me':
                    Route(sequence_builder=self.__service_locator.locate(GetAuthBrandSequenceBuilder)),

                'POST /brands/me':
                    Route(sequence_builder=self.__service_locator.locate(CreateBrandSequenceBuilder)),

                'PATCH /brands/me':
                    Route(sequence_builder=self.__service_locator.locate(UpdateBrandSequenceBuilder)),

                'POST /brands/me/images/{image_field}':
                    Route(sequence_builder=self.__service_locator.locate(UpdateBrandImageSequenceBuilder)),

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

        campaign_routes = OrderedDict(
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

        collaboration_routes = OrderedDict(
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

        notification_routes = OrderedDict(
            {
                'GET /notifications/{notification_id}':
                    Route(sequence_builder=self.__service_locator.locate(GetNotificationByIdSequenceBuilder)),

                'POST /users/me/notifications':
                    Route(sequence_builder=self.__service_locator.locate(CreateNotificationSequenceBuilder)),

                'PATCH /users/me/notifications':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'GET /receivers/me/notifications':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'GET /senders/me/notifications':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))
            }
        )

        audience_routes = OrderedDict(
            {
                'GET /influencers/me/audience-age-splits':
                    Route(sequence_builder=self.__service_locator.locate(GetAudienceAgeSequenceBuilder)),

                'GET /influencers/me/audience-gender-splits':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'POST /influencers/me/audience-age-splits':
                    Route(sequence_builder=self.__service_locator.locate(CreateAudienceAgeSequenceBuilder)),

                'POST /influencers/me/audience-gender-splits':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'PATCH /influencers/me/audience-age-splits':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'PATCH /influencers/me/audience-gender-splits':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder))
            }
        )

        routes = {}
        routes.update(feed_routes)
        routes.update(user_routes)
        routes.update(campaign_routes)
        routes.update(collaboration_routes)
        routes.update(notification_routes)
        routes.update(audience_routes)
        return routes
