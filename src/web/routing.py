from collections import OrderedDict

from src.web import Route, PinfluencerContext
from src.web.ioc import ServiceLocator


class Dispatcher:
    def __init__(self, service_locator: ServiceLocator):
        self.__campaign_ctr = service_locator.get_new_campaign_controller()
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
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response_collection,
                        self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images_collection,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories_collection
                    ]),

                'GET /influencers': Route(
                    action=self.__influencer_ctr.get_all,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response_collection,
                        self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images_collection,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories_collection
                    ]),

                'GET /brands/{brand_id}': Route(
                    before_hooks=[
                        self.__hooks_facade.get_brand_before_hooks().validate_uuid
                    ],
                    action=self.__brand_ctr.get_by_id,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]),

                'GET /influencers/{influencer_id}': Route(
                    before_hooks=[
                        self.__hooks_facade.get_influencer_before_hooks().validate_uuid
                    ],
                    action=self.__influencer_ctr.get_by_id,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]),

                # authenticated brand endpoints
                'GET /brands/me': Route(
                    before_hooks=[
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id
                    ],
                    action=self.__brand_ctr.get,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]
                ),

                'POST /brands/me': Route(
                    before_hooks=[
                        self.__hooks_facade.get_before_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                        self.__hooks_facade.get_brand_before_hooks().validate_brand
                    ],
                    action=self.__brand_ctr.create,
                    after_hooks=[
                        self.__hooks_facade.get_brand_after_hooks().set_brand_claims,
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]
                ),

                'PUT /brands/me': Route(
                    before_hooks=[
                        self.__hooks_facade.get_before_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                        self.__hooks_facade.get_brand_before_hooks().validate_brand
                    ],
                    action=self.__brand_ctr.update,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]
                ),

                'POST /brands/me/header-image': Route(
                    before_hooks=[
                        self.__hooks_facade.get_before_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id
                    ],
                    action=self.__brand_ctr.update_header_image,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]
                ),

                'POST /brands/me/logo': Route(
                    before_hooks=[
                        self.__hooks_facade.get_before_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id
                    ],
                    action=self.__brand_ctr.update_logo,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]
                ),

                # authenticated influencer endpoints
                'GET /influencers/me': Route(
                    before_hooks=[
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id
                    ],
                    action=self.__influencer_ctr.get,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]
                ),

                'POST /influencers/me': Route(
                    before_hooks=[
                        self.__hooks_facade.get_before_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                        self.__hooks_facade.get_influencer_before_hooks().validate_influencer
                    ],
                    action=self.__influencer_ctr.create,
                    after_hooks=[
                        self.__hooks_facade.get_influencer_after_hooks().set_influencer_claims,
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]
                ),

                'PUT /influencers/me': Route(
                    before_hooks=[
                        self.__hooks_facade.get_before_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                        self.__hooks_facade.get_influencer_before_hooks().validate_influencer
                    ],
                    action=self.__influencer_ctr.update,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]
                ),

                'POST /influencers/me/image': Route(
                    before_hooks=[
                        self.__hooks_facade.get_before_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                    ],
                    action=self.__influencer_ctr.update_profile_image,
                    after_hooks=[
                        self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                        self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images,
                        self.__hooks_facade.get_user_after_hooks().format_values_and_categories
                    ]
                ),
            }
        )

        campaigns = OrderedDict(
            {
                'GET /brands/me/campaigns': self.get_not_implemented_method('GET /brands/me/campaigns'),

                'DELETE /brands/me/campaigns/{campaign_id}':
                    self.get_not_implemented_method('DELETE brands/me/campaigns/{campaign_id}'),

                'GET /campaigns/{campaign_id}': Route(
                    before_hooks=[
                        self.__hooks_facade.get_campaign_before_hooks().validate_id
                    ],
                    action=self.__campaign_ctr.get_by_id,
                    after_hooks=[
                        self.__hooks_facade.get_campaign_after_hooks().format_values_and_categories,
                        self.__hooks_facade.get_campaign_after_hooks().tag_bucket_url_to_images
                    ]
                ),

                'POST /brands/me/campaigns': Route(
                    before_hooks=[
                        self.__hooks_facade.get_before_common_hooks().set_body,
                        self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                        self.__hooks_facade.get_campaign_before_hooks().validate_campaign
                    ],
                    action=self.__campaign_ctr.create
                ),

                'PUT /brands/me/campaigns/{campaign_id}': self.get_not_implemented_method('PUT /brands/me/campaigns/{campaign_id}'),

                'POST /campaigns/{campaign_id}/product-image1':
                    self.get_not_implemented_method('POST /campaigns/{campaign_id}/product-image1'),
                'POST /campaigns/{campaign_id}/product-image2':
                    self.get_not_implemented_method('POST /campaigns/{campaign_id}/product-image2'),
                'POST /campaigns/{campaign_id}/product-image3':
                    self.get_not_implemented_method('POST /campaigns/{campaign_id}/product-image3')
            }
        )

        routes = {}
        routes.update(feed)
        routes.update(users)
        routes.update(campaigns)
        return routes
