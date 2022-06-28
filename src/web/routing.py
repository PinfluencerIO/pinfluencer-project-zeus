from collections import OrderedDict

from src.web import Route, PinfluencerContext
from src.web.ioc import ServiceLocator


class Dispatcher:
    def __init__(self, service_locator: ServiceLocator):
        self.__brand_ctr = service_locator.get_new_brand_controller()
        self.__influencer_ctr = service_locator.get_new_influencer_controller()
        self.__hooks_facade = service_locator.get_new_hooks_facade()

    def get_not_implemented_method(self, route: str) -> Route:
        return Route(action=lambda context: self.not_implemented(context=context,
                                                                 route=route))

    @staticmethod
    def not_implemented(context: PinfluencerContext, route: str):
        context.response.status_code = 405
        context.response.body = {"message": f"{route} is not implemented"}

    @property
    def dispatch_route_to_ctr(self) -> dict[dict[str, Route]]:
        feed = OrderedDict(
            {'GET /feed': self.get_not_implemented_method('GET /feed')}
        )

        users = OrderedDict(
            {
                'GET /brands': Route(
                    action=self.__brand_ctr.get_all,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response_collection
                    ]),

                'GET /influencers': Route(
                    action=self.__influencer_ctr.get_all,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response_collection
                    ]),

                'GET /brands/{brand_id}': Route(
                    before_hooks=[
                        self.__hooks_facade.get_brand_before_hooks().validate_uuid
                    ],
                    action=self.__brand_ctr.get_by_id,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response
                    ]),

                'GET /influencers/{influencer_id}': Route(
                    before_hooks=[
                        self.__hooks_facade.get_influencer_before_hooks().validate_uuid
                    ],
                    action=self.__influencer_ctr.get_by_id,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response
                    ]),

                # authenticated brand endpoints
                'GET /brands/me': Route(
                    before_hooks=[
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id
                    ],
                    action=self.__brand_ctr.get,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response
                    ]
                ),

                'POST /brands/me': Route(
                    before_hooks=[
                        self.__hooks_facade.get_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                        self.__hooks_facade.get_brand_before_hooks().validate_brand
                    ],
                    action=self.__brand_ctr.create,
                    after_hooks=[
                        self.__hooks_facade.get_brand_after_hooks().set_brand_claims,
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response
                    ]
                ),

                'PUT /brands/me': Route(
                    before_hooks=[
                        self.__hooks_facade.get_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                        self.__hooks_facade.get_brand_before_hooks().validate_brand
                    ],
                    action=self.__brand_ctr.update,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response
                    ]
                ),

                'POST /brands/me/header-image': Route(
                    before_hooks=[
                        self.__hooks_facade.get_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id
                    ],
                    action=self.__brand_ctr.update_header_image,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response
                    ]
                ),

                'POST /brands/me/logo': Route(
                    before_hooks=[
                        self.__hooks_facade.get_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id
                    ],
                    action=self.__brand_ctr.update_logo,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response
                    ]
                ),

                # authenticated influencer endpoints
                'GET /influencers/me': Route(
                    before_hooks=[
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id
                    ],
                    action=self.__influencer_ctr.get,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response
                    ]
                ),

                'POST /influencers/me': Route(action=self.__influencer_ctr.create),

                'PUT /influencers/me': Route(action=self.__influencer_ctr.update),

                'POST /influencers/me/image': Route(action=self.__influencer_ctr.update_profile_image),
            }
        )

        campaigns = OrderedDict(
            {
                'GET /campaigns/me': self.get_not_implemented_method('GET /campaigns/me'),

                'DELETE /campaigns/me/{campaign_id}': self.get_not_implemented_method(
                    'DELETE /campaigns/me/{campaign_id}'),

                'GET /campaigns/me/{campaign_id}': self.get_not_implemented_method('GET /campaigns/me/{campaign_id}'),

                'POST /campaigns/me': self.get_not_implemented_method('POST /campaigns/me'),

                'PUT /campaigns/me/{campaign_id}': self.get_not_implemented_method('PUT /campaigns/me/{campaign_id}')
            }
        )

        routes = {}
        routes.update(feed)
        routes.update(users)
        routes.update(campaigns)
        return routes
