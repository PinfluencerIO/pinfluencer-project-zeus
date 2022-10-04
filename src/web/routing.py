from collections import OrderedDict

from src import ServiceLocator
from src.web import Route
from src.web.controllers import CampaignController, BrandController, InfluencerController
from src.web.hooks import HooksFacade
from src.web.sequences import UpdateCampaignSequenceBuilder, UpdateImageForCampaignSequenceBuilder, \
    NotImplementedSequenceBuilder, CreateCampaignSequenceBuilder, GetCampaignByIdSequenceBuilder, \
    GetCampaignsForBrandSequenceBuilder, UpdateInfluencerImageSequenceBuilder, UpdateInfluencerSequenceBuilder, \
    CreateInfluencerSequenceBuilder, GetAuthInfluencerSequenceBuilder, GetInfluencerByIdSequenceBuilder, \
    GetAllInfluencersSequenceBuilder, UpdateBrandImageSequenceBuilder, UpdateBrandSequenceBuilder, \
    CreateBrandSequenceBuilder, GetAuthBrandSequenceBuilder, GetBrandByIdSequenceBuilder, GetAllBrandsSequenceBuilder


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
