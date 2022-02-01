from collections import OrderedDict

from src.web import PinfluencerResponse
from src.web.controllers import BrandController


class Routes:
    def __init__(self):
        self.__brand_ctr = BrandController(brand_repository=None)

    @property
    def routes(self):

        feed = OrderedDict(
            {'GET /feed': lambda: PinfluencerResponse(status_code=200)}
        )

        users = OrderedDict(
            {
                'GET /brands': self.__brand_ctr.handle_get_all_brands,

                'GET /influencers': lambda: PinfluencerResponse(status_code=200),

                'GET /brands/{brand_id}': self.__brand_ctr.handle_get_by_id,

                'GET /influencers/{influencer_id}': lambda: PinfluencerResponse(status_code=200),

                # authenticated brand endpoints
                'GET /brands/me': self.__brand_ctr.handle_get_brand,

                'POST /brands/me': self.__brand_ctr.handle_create_brand,

                'PUT /brands/me': self.__brand_ctr.handle_update_brand,

                'PATCH /brands/me/image': self.__brand_ctr.handle_update_brand_image,

                # authenticated influencer endpoints
                'GET /influencers/me': lambda: PinfluencerResponse(status_code=200),

                'POST /influencers/me': lambda: PinfluencerResponse(status_code=200),

                'PUT /influencers/me': lambda: PinfluencerResponse(status_code=200),

                'PATCH /influencers/me/image': lambda: PinfluencerResponse(status_code=200),
            }
        )

        campaigns = OrderedDict(
            {'GET /campaigns/me': lambda: PinfluencerResponse(status_code=200)}
        )

        routes = {}
        routes.update(feed)
        routes.update(users)
        routes.update(campaigns)
        return routes
