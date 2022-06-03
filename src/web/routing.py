from collections import OrderedDict
from typing import Callable

from src.service import ServiceLocator
from src.web import PinfluencerResponse


class Dispatcher:
    def __init__(self, service_locator: ServiceLocator):
        self.__brand_ctr = service_locator.get_new_brand_controller()

    @staticmethod
    def __get_not_implemented_method(route: str) -> Callable[[dict], PinfluencerResponse]:
        return lambda event: PinfluencerResponse(status_code=405, body={"message": f"{route} is not implemented"})

    @property
    def dispatch_route_to_ctr(self) -> dict[dict[str, Callable[[dict], PinfluencerResponse]]]:

        feed = OrderedDict(
            {'GET /feed': self.__get_not_implemented_method('GET /feed')}
        )

        users = OrderedDict(
            {
                'GET /brands': self.__brand_ctr.get_all,

                'GET /influencers': self.__get_not_implemented_method('GET /influencers'),

                'GET /brands/{brand_id}': self.__brand_ctr.get_by_id,

                'GET /influencers/{influencer_id}': self.__get_not_implemented_method('GET /influencers/{influencer_id}'),

                # authenticated brand endpoints
                'GET /brands/me': self.__brand_ctr.get,

                'POST /brands/me': self.__brand_ctr.create,

                'PUT /brands/me': self.__brand_ctr.update,

                'POST /brands/me/header_image': self.__brand_ctr.update_header_image,

                'POST /brands/me/logo': self.__brand_ctr.update_logo,

                # authenticated influencer endpoints
                'GET /influencers/me': self.__get_not_implemented_method('GET /influencers/me'),

                'POST /influencers/me': self.__get_not_implemented_method('POST /influencers/me'),

                'PUT /influencers/me': self.__get_not_implemented_method('PUT /influencers/me'),

                'POST /influencers/me/image': self.__get_not_implemented_method('POST /influencers/me/image'),
            }
        )

        campaigns = OrderedDict(
            {'GET /campaigns/me': self.__get_not_implemented_method('GET /campaigns/me')}
        )

        routes = {}
        routes.update(feed)
        routes.update(users)
        routes.update(campaigns)
        return routes
