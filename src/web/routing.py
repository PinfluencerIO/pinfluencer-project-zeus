from collections import OrderedDict

from src.web import Route, PinfluencerContext
from src.web.controllers import CampaignController, BrandController, InfluencerController
from src.web.hooks import HooksFacade


class Dispatcher:
    def __init__(self, campaign_ctr: CampaignController,
                 brand_ctr: BrandController,
                 influencer_ctr: InfluencerController,
                 hooks_facade: HooksFacade):
        self.__campaign_ctr = campaign_ctr
        self.__brand_ctr = brand_ctr
        self.__influencer_ctr = influencer_ctr
        self.__hooks_facade = hooks_facade

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
                'GET /brands': self.get_all_brands(),

                'GET /influencers': self.get_all_influencers(),

                'GET /brands/{brand_id}': self.get_brand_by_id(),

                'GET /influencers/{influencer_id}': self.get_influencer_by_id(),

                # authenticated brand endpoints
                'GET /brands/me': self.get_auth_brand(),

                'POST /brands/me': self.create_brand(),

                'PATCH /brands/me': self.update_brand(),

                'POST /brands/me/images/{image_field}': self.update_brand_image(),

                # authenticated influencer endpoints
                'GET /influencers/me': self.get_auth_influencer(),

                'POST /influencers/me': self.create_influencer(),

                'PATCH /influencers/me': self.update_influencer(),

                'POST /influencers/me/images/{image_field}': self.update_influencer_image(),
            }
        )


        campaigns = OrderedDict(
            {
                'GET /brands/me/campaigns': self.get_campaigns_for_brand(),

                'DELETE /brands/me/campaigns/{campaign_id}': self.delete_campaign_for_brand(),

                'GET /campaigns/{campaign_id}': self.get_campaign_by_id(),

                'POST /brands/me/campaigns': self.create_campaign(),

                'PATCH /brands/me/campaigns/{campaign_id}': self.update_campgin_bulk(),

                'POST /brands/me/campaigns/{campaign_id}/images/{image_field}': self.update_image_for_campaign()
            }
        )
        routes = {}
        routes.update(feed)
        routes.update(users)
        routes.update(campaigns)
        return routes

    def update_prod3_image_for_campaign(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_campaign_before_hooks().validate_id,
                self.__hooks_facade.get_brand_before_hooks().validate_auth_brand
            ],
            action=self.__campaign_ctr.update_image_field,
            after_hooks=[
                self.__hooks_facade.get_campaign_after_hooks().format_values_and_categories,
                self.__hooks_facade.get_campaign_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_campaign_after_hooks().format_campaign_state
            ]
        )

    def update_prod2_image_for_campaign(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_campaign_before_hooks().validate_id,
                self.__hooks_facade.get_brand_before_hooks().validate_auth_brand
            ],
            action=self.__campaign_ctr.update_image_field,
            after_hooks=[
                self.__hooks_facade.get_campaign_after_hooks().format_values_and_categories,
                self.__hooks_facade.get_campaign_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_campaign_after_hooks().format_campaign_state
            ]
        )

    def update_image_for_campaign(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_campaign_before_hooks().validate_id,
                self.__hooks_facade.get_brand_before_hooks().validate_auth_brand,
                self.__hooks_facade.get_campaign_before_hooks().validate_image_key,
                self.__hooks_facade.get_campaign_before_hooks().upload_image
            ],
            action=self.__campaign_ctr.update_image_field,
            after_hooks=[
                self.__hooks_facade.get_campaign_after_hooks().format_values_and_categories,
                self.__hooks_facade.get_campaign_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_campaign_after_hooks().format_campaign_state
            ]
        )

    def update_campgin_bulk(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_campaign_before_hooks().validate_id,
                self.__hooks_facade.get_campaign_before_hooks().validate_campaign,
                self.__hooks_facade.get_brand_before_hooks().validate_auth_brand,
                self.__hooks_facade.get_campaign_before_hooks().map_campaign_state,
                self.__hooks_facade.get_campaign_before_hooks().map_campaign_categories_and_values
            ],
            action=self.__campaign_ctr.update,
            after_hooks=[
                self.__hooks_facade.get_campaign_after_hooks().format_values_and_categories,
                self.__hooks_facade.get_campaign_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_campaign_after_hooks().format_campaign_state
            ]
        )

    def create_campaign(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_campaign_before_hooks().validate_campaign,
                self.__hooks_facade.get_campaign_before_hooks().map_campaign_state,
                self.__hooks_facade.get_campaign_before_hooks().map_campaign_categories_and_values
            ],
            action=self.__campaign_ctr.create,
            after_hooks=[
                self.__hooks_facade.get_campaign_after_hooks().format_values_and_categories,
                self.__hooks_facade.get_campaign_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_campaign_after_hooks().format_campaign_state
            ]
        )

    def get_campaign_by_id(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_campaign_before_hooks().validate_id
            ],
            action=self.__campaign_ctr.get_by_id,
            after_hooks=[
                self.__hooks_facade.get_campaign_after_hooks().format_values_and_categories,
                self.__hooks_facade.get_campaign_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_campaign_after_hooks().format_campaign_state
            ]
        )

    def delete_campaign_for_brand(self):
        return self.get_not_implemented_method('DELETE brands/me/campaigns/{campaign_id}')

    def get_campaigns_for_brand(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id
            ],
            action=self.__campaign_ctr.get_for_brand,
            after_hooks=[
                self.__hooks_facade.get_campaign_after_hooks().format_values_and_categories_collection,
                self.__hooks_facade.get_campaign_after_hooks().tag_bucket_url_to_images_collection,
                self.__hooks_facade.get_campaign_after_hooks().format_campaign_state_collection
            ]
        )

    def update_influencer_image(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_influencer_before_hooks().validate_image_key,
                self.__hooks_facade.get_influencer_before_hooks().upload_image
            ],
            action=self.__influencer_ctr.update_image_field,
            after_hooks=[
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
            ]
        )

    def update_influencer(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_influencer_before_hooks().validate_influencer,
                self.__hooks_facade.get_user_before_hooks().set_categories_and_values,
            ],
            action=self.__influencer_ctr.update,
            after_hooks=[
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
            ]
        )

    def create_influencer(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_influencer_before_hooks().validate_influencer,
                self.__hooks_facade.get_user_before_hooks().set_categories_and_values
            ],
            action=self.__influencer_ctr.create,
            after_hooks=[
                self.__hooks_facade.get_influencer_after_hooks().set_influencer_claims,
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
            ]
        )

    def get_auth_influencer(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id
            ],
            action=self.__influencer_ctr.get,
            after_hooks=[
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
            ]
        )

    def update_brand_image(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_brand_before_hooks().validate_image_key,
                self.__hooks_facade.get_brand_before_hooks().upload_image
            ],
            action=self.__brand_ctr.update_image_field,
            after_hooks=[
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
            ]
        )

    def update_brand(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_brand_before_hooks().validate_brand,
                self.__hooks_facade.get_user_before_hooks().set_categories_and_values
            ],
            action=self.__brand_ctr.update,
            after_hooks=[
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
            ]
        )

    def create_brand(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_before_common_hooks().set_body,
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id,
                self.__hooks_facade.get_brand_before_hooks().validate_brand,
                self.__hooks_facade.get_user_before_hooks().set_categories_and_values
            ],
            action=self.__brand_ctr.create,
            after_hooks=[
                self.__hooks_facade.get_brand_after_hooks().set_brand_claims,
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
            ]
        )

    def get_auth_brand(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_user_before_hooks().set_auth_user_id
            ],
            action=self.__brand_ctr.get,
            after_hooks=[
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
            ]
        )

    def get_influencer_by_id(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_influencer_before_hooks().validate_uuid
            ],
            action=self.__influencer_ctr.get_by_id,
            after_hooks=[
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
            ])

    def get_brand_by_id(self):
        return Route(
            before_hooks=[
                self.__hooks_facade.get_brand_before_hooks().validate_uuid
            ],
            action=self.__brand_ctr.get_by_id,
            after_hooks=[
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories
            ])

    def get_all_influencers(self):
        return Route(
            action=self.__influencer_ctr.get_all,
            after_hooks=[
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response_collection,
                self.__hooks_facade.get_influencer_after_hooks().tag_bucket_url_to_images_collection,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories_collection
            ])

    def get_all_brands(self):
        return Route(
            action=self.__brand_ctr.get_all,
            after_hooks=[
                self.__hooks_facade.get_user_after_hooks().tag_auth_user_claims_to_response_collection,
                self.__hooks_facade.get_brand_after_hooks().tag_bucket_url_to_images_collection,
                self.__hooks_facade.get_user_after_hooks().format_values_and_categories_collection
            ])
