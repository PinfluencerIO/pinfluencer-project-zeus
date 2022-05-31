from collections import OrderedDict

from src.service import ServiceLocator
from src.web import PinfluencerResponse


class Dispatcher:
    def __init__(self, service_locator: ServiceLocator):
        self.__brand_ctr = service_locator.get_new_brand_controller()

    @property
    def dispatch_route_to_ctr(self):

        feed = OrderedDict(
            {'GET /feed': lambda event: PinfluencerResponse(status_code=200)}
        )

        users = OrderedDict(
            {
                'GET /brands': self.__brand_ctr.get_all,

                'GET /influencers': lambda event: PinfluencerResponse(status_code=200),

                'GET /brands/{brand_id}': self.__brand_ctr.get_by_id,

                'GET /influencers/{influencer_id}': lambda event: PinfluencerResponse(status_code=200),

                # authenticated brand endpoints
                'GET /brands/me': self.__brand_ctr.get,

                'POST /brands/me': self.__brand_ctr.create,

                'PUT /brands/me': self.__brand_ctr.update,

                'POST /brands/me/header_image': self.__brand_ctr.update_header_image,

                'POST /brands/me/logo': self.__brand_ctr.update_logo,

                # authenticated influencer endpoints
                'GET /influencers/me': lambda event: PinfluencerResponse(status_code=200),

                'POST /influencers/me': lambda event: PinfluencerResponse(status_code=200),

                'PUT /influencers/me': lambda event: PinfluencerResponse(status_code=200),

                'PATCH /influencers/me/image': lambda event: PinfluencerResponse(status_code=200),
            }
        )

        campaigns = OrderedDict(
            {'GET /campaigns/me': lambda event: PinfluencerResponse(status_code=200)}
        )

        routes = {}
        routes.update(feed)
        routes.update(users)
        routes.update(campaigns)
        return routes
