from collections import OrderedDict

from src.web import PinfluencerResponse
from src.web.controllers import BrandController


class Dispatcher:
    def __init__(self):
        self.__brand_ctr = BrandController(brand_repository=None)

    @property
    def dispatch_route_to_ctr(self):

        feed = OrderedDict(
            {'GET /feed': PinfluencerResponse}
        )

        users = OrderedDict(
            {
                'GET /brands': self.__brand_ctr.get_all,

                'GET /influencers': lambda: PinfluencerResponse(status_code=200),

                'GET /brands/{brand_id}': self.__brand_ctr.get_by_id,

                'GET /influencers/{influencer_id}': lambda: PinfluencerResponse(status_code=200),

                # authenticated brand endpoints
                'GET /brands/me': self.__brand_ctr.get,

                'POST /brands/me': self.__brand_ctr.create,

                'PUT /brands/me': self.__brand_ctr.update,

                'POST /brands/me/header_image': self.__brand_ctr.update_header_image,

                'POST /brands/me/logo': self.__brand_ctr.update_logo,

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
