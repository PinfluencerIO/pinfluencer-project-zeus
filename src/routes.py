from collections import OrderedDict

from src.data_access_layer.read_data_access import load_collection, load_by_id, \
    load_brand_for_authenticated_user
from src.data_access_layer.write_data_access import db_write_new_brand_for_auth_user, \
    db_write_update_brand_for_auth_user, db_write_patch_brand_image_for_auth_user
from src.pinfluencer_response import PinfluencerResponse
from src.processors.get_by_id import ProcessGetBy
from src.processors.get_collection import ProcessGetCollection
from src.processors.get_for_auth_user import ProcessGetForAuthenticatedUser
from src.processors.ok_response import ProcessOkResponse
from src.processors.write_for_auth_user import ProcessWriteForAuthenticatedUser


class Controller:
    def __init__(self, data_manager) -> None:
        self._data_manager = data_manager


class FeedController(Controller):
    def __init__(self, data_manager) -> None:
        super().__init__(data_manager)

    def handle_feed(self, event):
        return ProcessOkResponse().do_process(event)


class BrandController(Controller):
    def __init__(self, data_manager, image_repo, brand_repository) -> None:
        super().__init__(data_manager)
        self.__brand_repository = brand_repository
        self._image_repository = image_repo

    def handle_get_all_brands(self, event):
        return ProcessGetCollection('brand', load_collection, self._data_manager).do_process(event)

    def handle_get_by_id(self, event):
        return PinfluencerResponse(status_code=400, body={})

    def handle_get_brand(self, event):
        return ProcessGetForAuthenticatedUser(load_brand_for_authenticated_user, self._data_manager).do_process(event)

    def handle_create_brand(self, event):
        return ProcessWriteForAuthenticatedUser('brand', 'post', db_write_new_brand_for_auth_user,
                                                self._data_manager,
                                                self._image_repository).do_process(event)

    def handle_update_brand(self, event):
        return ProcessWriteForAuthenticatedUser('brand', 'put', db_write_update_brand_for_auth_user,
                                                self._data_manager,
                                                self._image_repository).do_process(event)

    def handle_update_brand_image(self, event):
        return ProcessWriteForAuthenticatedUser('brand', 'patch',
                                                db_write_patch_brand_image_for_auth_user,
                                                self._data_manager,
                                                self._image_repository).do_process(event)


class InfluencerController(Controller):
    def __init__(self, data_manager, image_repo) -> None:
        super().__init__(data_manager)
        self._image_repository = image_repo

    def handle_get_all_influencers(self, event):
        return ProcessGetCollection('influencers', load_collection, self._data_manager).do_process(event)

    def handle_get_by_id(self, event):
        return ProcessGetBy(load_by_id, 'influencers', self._data_manager).do_process(event)

    def handle_get_influencer(self, event):
        raise NotImplemented

    def handle_create_influencer(self, event):
        raise NotImplemented

    def handle_update_influencer(self, event):
        raise NotImplemented

    def handle_update_influencer_image(self, event):
        raise NotImplemented


class CampaignController(Controller):
    def __init__(self, data_manager, image_repo) -> None:
        super().__init__(data_manager)
        self._image_repository = image_repo

    def handle_get_all_campaigns(self, event):
        raise NotImplemented


class Routes:
    def __init__(self, data_manager, image_repository):
        self.__feed_ctr = FeedController(data_manager)
        self.__brand_ctr = BrandController(data_manager, image_repository)
        self.__influencer_ctr = InfluencerController(data_manager, image_repository)
        self.__campaign_ctr = CampaignController(data_manager, image_repository)

    @property
    def routes(self):

        feed = OrderedDict(
            {'GET /feed': self.__feed_ctr.handle_feed}
        )

        users = OrderedDict(
            {
                'GET /brands': self.__brand_ctr.handle_get_all_brands,

                'GET /influencers': self.__influencer_ctr.handle_get_all_influencers,

                'GET /brands/{brand_id}': self.__brand_ctr.handle_get_by_id,

                'GET /influencers/{influencer_id}': self.__influencer_ctr.handle_get_by_id,

                # authenticated brand endpoints
                'GET /brands/me': self.__brand_ctr.handle_get_brand,

                'POST /brands/me': self.__brand_ctr.handle_create_brand,

                'PUT /brands/me': self.__brand_ctr.handle_update_brand,

                'PATCH /brands/me/image': self.__brand_ctr.handle_update_brand_image,

                # authenticated influencer endpoints
                'GET /influencers/me': self.__influencer_ctr.handle_get_influencer,

                'POST /influencers/me': self.__influencer_ctr.handle_create_influencer,

                'PUT /influencers/me': self.__influencer_ctr.handle_update_influencer,

                'PATCH /influencers/me/image': self.__influencer_ctr.handle_update_influencer_image,
            }
        )

        campaigns = OrderedDict(
            {'GET /campaigns/me': self.__campaign_ctr.handle_get_all_campaigns}
        )

        routes = {}
        routes.update(feed)
        routes.update(users)
        routes.update(campaigns)
        return routes
