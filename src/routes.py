from collections import OrderedDict

from src.data_access_layer.read_data_access import load_max_3_products_for_brand, load_collection, load_by_id, \
    load_brand_for_authenticated_user
from src.data_access_layer.write_data_access import db_write_new_brand_for_auth_user, \
    db_write_update_brand_for_auth_user, db_write_patch_brand_image_for_auth_user
from src.processors.get_by_id import ProcessGetBy
from src.processors.get_collection import ProcessGetCollection
from src.processors.get_for_auth_user import ProcessGetForAuthenticatedUser
from src.processors.ok_response import ProcessOkResponse
from src.processors.write_for_auth_user import ProcessWriteForAuthenticatedUser


class Routes:
    def __init__(self, container):
        self.__container = container

    @property
    def routes(self):
        return OrderedDict({
            # public endpoints
            'GET /feed': ProcessGetCollection('brand', load_max_3_products_for_brand, self.__container.data_manager),

            'GET /brands': ProcessGetCollection('brand', load_collection, self.__container.data_manager),

            'GET /brands/{brand_id}': ProcessGetBy(load_by_id, 'brand', self.__container.data_manager),

            'GET /brands/{brand_id}/campaigns': ProcessOkResponse(),

            'GET /campaigns': ProcessOkResponse(),

            'GET /campaigns/{campaign_id}': ProcessOkResponse(),

            # authenticated brand endpoints
            'GET /brands/me': ProcessGetForAuthenticatedUser(load_brand_for_authenticated_user,
                                                             self.__container.data_manager),

            'POST /brands/me': ProcessWriteForAuthenticatedUser('brand', 'post', db_write_new_brand_for_auth_user,
                                                                self.__container.data_manager,
                                                                self.__container.image_repository),

            'PUT /brands/me': ProcessWriteForAuthenticatedUser('brand', 'put', db_write_update_brand_for_auth_user,
                                                               self.__container.data_manager,
                                                               self.__container.image_repository),

            'PATCH /brands/me/image': ProcessWriteForAuthenticatedUser('brand', 'patch',
                                                                       db_write_patch_brand_image_for_auth_user,
                                                                       self.__container.data_manager,
                                                                       self.__container.image_repository),

            # authenticated campaign endpoints
            'GET /campaigns/me': ProcessOkResponse(),

            'GET /campaigns/me/{campaign_id}': ProcessOkResponse(),

            'POST /campaigns/me': ProcessOkResponse(),

            'PUT /campaigns/me/{campaign_id}': ProcessOkResponse(),

            'PATCH /campaigns/me/{campaign_id}/image': ProcessOkResponse(),

            'DELETE /campaigns/me/{campaign_id}': ProcessOkResponse(),
        })
