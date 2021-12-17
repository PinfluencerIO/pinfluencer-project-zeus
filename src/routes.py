from collections import OrderedDict

from src.container import Container
from src.data_access_layer.read_data_access import load_max_3_products_for_brand, load_collection, load_by_id, \
    load_all_products_for_brand_id, load_brand_for_authenticated_user, load_products_for_authenticated_user, \
    load_product_by_id_for_auth_id
from src.data_access_layer.write_data_access import db_write_new_brand_for_auth_user, \
    db_write_update_brand_for_auth_user, db_write_patch_brand_image_for_auth_user, db_write_new_product_for_auth_user, \
    db_write_update_product_for_auth_user, db_write_patch_product_image_for_auth_user, delete_product
from src.processors.delete_product import ProcessAuthenticatedDeleteProduct
from src.processors.get_by_id import ProcessGetBy
from src.processors.get_by_id_for_auth_user import ProcessGetByForAuthenticatedUser
from src.processors.get_collection import ProcessGetCollection
from src.processors.get_for_auth_user import ProcessGetForAuthenticatedUser, ProcessGetForAuthenticatedUserAsCollection
from src.processors.get_products_for_brand import ProcessGetProductsForBrand
from src.processors.write_for_auth_user import ProcessWriteForAuthenticatedUser, \
    ProcessWriteWithValidationForAuthenticatedUser, ProcessWriteForAuthenticatedUserWithProductId


class Routes:
    def __init__(self, container: Container):
        self.__container = container
        pass

    @property
    def routes(self) -> OrderedDict:
        return OrderedDict({
            # public endpoints
            'GET /feed': ProcessGetCollection('brand', load_max_3_products_for_brand, self.__container.data_manager),

            'GET /brands': ProcessGetCollection('brand', load_collection, self.__container.data_manager),

            'GET /brands/{brand_id}': ProcessGetBy(load_by_id, 'brand', self.__container.data_manager),

            'GET /brands/{brand_id}/products': ProcessGetProductsForBrand(load_all_products_for_brand_id,
                                                                          self.__container.data_manager),

            'GET /products': ProcessGetCollection('product', load_collection, self.__container.data_manager),

            'GET /products/{product_id}': ProcessGetBy(load_by_id, 'product', self.__container.data_manager),

            # authenticated brand endpoints
            'GET /brands/me': ProcessGetForAuthenticatedUser(load_brand_for_authenticated_user,
                                                             self.__container.data_manager),

            'POST /brands/me': ProcessWriteForAuthenticatedUser('brand', 'post', db_write_new_brand_for_auth_user,
                                                                self.__container.data_manager),

            'PUT /brands/me': ProcessWriteForAuthenticatedUser('brand', 'put', db_write_update_brand_for_auth_user,
                                                               self.__container.data_manager),

            'PATCH /brands/me/image': ProcessWriteForAuthenticatedUser('brand', 'patch',
                                                                       db_write_patch_brand_image_for_auth_user,
                                                                       self.__container.data_manager),

            # authenticated product endpoints
            'GET /products/me': ProcessGetForAuthenticatedUserAsCollection(load_products_for_authenticated_user,
                                                                           self.__container.data_manager),

            'GET /products/me/{product_id}': ProcessGetByForAuthenticatedUser(load_product_by_id_for_auth_id, 'product',
                                                                              self.__container.data_manager),

            'POST /products/me': ProcessWriteWithValidationForAuthenticatedUser('product', 'post',
                                                                                db_write_new_product_for_auth_user,
                                                                                self.__container.data_manager),

            'PUT /products/me/{product_id}':
                ProcessWriteForAuthenticatedUserWithProductId('product', 'put', db_write_update_product_for_auth_user,
                                                              self.__container.data_manager),

            'PATCH /products/me/{product_id}/image':
                ProcessWriteForAuthenticatedUserWithProductId('product', 'patch',
                                                              db_write_patch_product_image_for_auth_user,
                                                              self.__container.data_manager),

            'DELETE /products/me/{product_id}': ProcessAuthenticatedDeleteProduct(delete_product,
                                                                                  self.__container.data_manager),
        })
