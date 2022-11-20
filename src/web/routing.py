from collections import OrderedDict

from src import ServiceLocator
from src.web import Route
from src.web.sequences import UpdateListingSequenceBuilder, UpdateImageForListingSequenceBuilder, \
    NotImplementedSequenceBuilder, CreateListingSequenceBuilder, GetListingByIdSequenceBuilder, \
    GetListingsForBrandSequenceBuilder, UpdateInfluencerImageSequenceBuilder, UpdateInfluencerSequenceBuilder, \
    CreateInfluencerSequenceBuilder, GetAuthInfluencerSequenceBuilder, GetInfluencerByIdSequenceBuilder, \
    GetAllInfluencersSequenceBuilder, UpdateBrandImageSequenceBuilder, UpdateBrandSequenceBuilder, \
    CreateBrandSequenceBuilder, GetAuthBrandSequenceBuilder, GetBrandByIdSequenceBuilder, GetAllBrandsSequenceBuilder, \
    CreateNotificationSequenceBuilder, GetNotificationByIdSequenceBuilder, CreateAudienceAgeSequenceBuilder, \
    GetAudienceAgeSequenceBuilder, UpdateAudienceAgeSequenceBuilder, CreateAudienceGenderSequenceBuilder, \
    GetAudienceGenderSequenceBuilder, UpdateAudienceGenderSequenceBuilder, CreateInfluencerProfileSequenceBuilder


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

        onboarding_routes = OrderedDict({
            'POST /influencer-profile':
                Route(self.__service_locator.locate(CreateInfluencerProfileSequenceBuilder)),

            'PATCH /influencer-profile':
                Route(self.__service_locator.locate(NotImplementedSequenceBuilder)),

            'GET /influencer-profile':
                Route(self.__service_locator.locate(NotImplementedSequenceBuilder)),

        })

        listing_routes = OrderedDict(
            {
                'GET /brands/me/listings':
                    Route(sequence_builder=self.__service_locator.locate(GetListingsForBrandSequenceBuilder)),

                'DELETE /brands/me/listings/{listing_id}':
                    Route(sequence_builder=self.__service_locator.locate(NotImplementedSequenceBuilder)),

                'GET /listings/{listing_id}':
                    Route(sequence_builder=self.__service_locator.locate(GetListingByIdSequenceBuilder)),

                'POST /brands/me/listings':
                    Route(sequence_builder=self.__service_locator.locate(CreateListingSequenceBuilder)),

                'PATCH /brands/me/listings/{listing_id}':
                    Route(sequence_builder=self.__service_locator.locate(UpdateListingSequenceBuilder)),

                'POST /brands/me/listings/{listing_id}/images/{image_field}':
                    Route(sequence_builder=self.__service_locator.locate(UpdateImageForListingSequenceBuilder))
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
                    Route(sequence_builder=self.__service_locator.locate(GetAudienceGenderSequenceBuilder)),

                'POST /influencers/me/audience-age-splits':
                    Route(sequence_builder=self.__service_locator.locate(CreateAudienceAgeSequenceBuilder)),

                'POST /influencers/me/audience-gender-splits':
                    Route(sequence_builder=self.__service_locator.locate(CreateAudienceGenderSequenceBuilder)),

                'PATCH /influencers/me/audience-age-splits':
                    Route(sequence_builder=self.__service_locator.locate(UpdateAudienceAgeSequenceBuilder)),

                'PATCH /influencers/me/audience-gender-splits':
                    Route(sequence_builder=self.__service_locator.locate(UpdateAudienceGenderSequenceBuilder))
            }
        )

        routes = {}
        routes.update(feed_routes)
        routes.update(user_routes)
        routes.update(listing_routes)
        routes.update(collaboration_routes)
        routes.update(notification_routes)
        routes.update(audience_routes)
        routes.update(onboarding_routes)
        return routes
