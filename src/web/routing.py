from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Callable

from src.service import ServiceLocator
from src.web import PinfluencerResponse


@dataclass
class Route:
    action: Callable[[dict], PinfluencerResponse]
    after_hooks: list[Callable[[PinfluencerResponse], None]] = field(default_factory=list)


class Dispatcher:
    def __init__(self, service_locator: ServiceLocator):
        self.__brand_ctr = service_locator.get_new_brand_controller()
        self.__influencer_ctr = service_locator.get_new_influencer_controller()

    @staticmethod
    def __get_not_implemented_method(route: str) -> Route:
        return Route(action=lambda event: PinfluencerResponse(status_code=405, body={"message": f"{route} is not implemented"}))

    @property
    def dispatch_route_to_ctr(self) -> dict[dict[str, Route]]:
        feed = OrderedDict(
            {'GET /feed': self.__get_not_implemented_method('GET /feed')}
        )

        users = OrderedDict(
            {
                'GET /brands': Route(action=self.__brand_ctr.get_all),

                'GET /influencers': Route(action=self.__influencer_ctr.get_all),

                'GET /brands/{brand_id}': Route(action=self.__brand_ctr.get_by_id),

                'GET /influencers/{influencer_id}': Route(action=self.__influencer_ctr.get_by_id),

                # authenticated brand endpoints
                'GET /brands/me': Route(action=self.__brand_ctr.get),

                'POST /brands/me': Route(action=self.__brand_ctr.create),

                'PUT /brands/me': Route(action=self.__brand_ctr.update),

                'POST /brands/me/header-image': Route(action=self.__brand_ctr.update_header_image),

                'POST /brands/me/logo': Route(action=self.__brand_ctr.update_logo),

                # authenticated influencer endpoints
                'GET /influencers/me': Route(action=self.__influencer_ctr.get),

                'POST /influencers/me': Route(action=self.__influencer_ctr.create),

                'PUT /influencers/me': Route(action=self.__influencer_ctr.update),

                'POST /influencers/me/image': Route(action=self.__influencer_ctr.update_profile_image),
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

