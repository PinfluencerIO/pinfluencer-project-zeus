from collections import OrderedDict
from typing import Callable

from src.service import ServiceLocator
from src.web import PinfluencerResponse


class Dispatcher:
    def __init__(self, service_locator: ServiceLocator):
        self.__brand_ctr = service_locator.get_new_brand_controller()
        self.__influencer_ctr = service_locator.get_new_influencer_controller()

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

                'GET /influencers': self.__influencer_ctr.get_all,

                'GET /brands/{brand_id}': self.__brand_ctr.get_by_id,

                'GET /influencers/{influencer_id}': self.__influencer_ctr.get_by_id,

                # authenticated brand endpoints
                'GET /brands/me': self.__brand_ctr.get,

                'POST /brands/me': self.__brand_ctr.create,

                'PUT /brands/me': self.__brand_ctr.update,

                'POST /brands/me/header-image': self.__brand_ctr.update_header_image,

                'POST /brands/me/logo': self.__brand_ctr.update_logo,

                # authenticated influencer endpoints
                'GET /influencers/me': self.__influencer_ctr.get,

                'POST /influencers/me': self.__influencer_ctr.create,

                'PUT /influencers/me': self.__influencer_ctr.update,

                'POST /influencers/me/image': self.__influencer_ctr.update_profile_image,
            }
        )

        campaigns = OrderedDict(
            {
                'GET /campaigns/me': self.__get_not_implemented_method('GET /campaigns/me'),

                'DELETE /campaigns/me/{campaign_id}': self.__get_not_implemented_method(
                    'DELETE /campaigns/me/{campaign_id}'),

                'GET /campaigns/me/{campaign_id}': self.__get_not_implemented_method('GET /campaigns/me/{campaign_id}'),

                'POST /campaigns/me': self.__get_not_implemented_method('POST /campaigns/me'),

                'PUT /campaigns/me/{campaign_id}': self.__get_not_implemented_method('PUT /campaigns/me/{campaign_id}')
            }
        )

        routes = {}
        routes.update(feed)
        routes.update(users)
        routes.update(campaigns)
        return routes

