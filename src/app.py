from collections import OrderedDict

from src.container import Container
from src.data_access_layer.write_data_access import update_brand_image
from src.filters.authorised_filter import *
from src.filters.payload_validation import *
from src.log_util import print_exception
from src.processors import *
from src.processors.brands import *
from src.processors.feed import ProcessPublicFeed
from src.processors.products import *


def lambda_handler(event, context):
    container = Container()
    try:
        routes = OrderedDict({
            # public endpoints
            'GET /feed': ProcessPublicFeed(container.data_manager),

            'GET /brands': ProcessPublicBrands(container.data_manager),

            'GET /brands/{brand_id}': ProcessPublicGetBrandBy(LoadResourceById(container.data_manager, 'brand')),

            'GET /brands/{brand_id}/products': ProcessPublicAllProductsForBrand(
                LoadResourceById(container.data_manager, 'brand'), container.data_manager),

            'GET /products': ProcessPublicProducts(container.data_manager),

            'GET /products/{product_id}': ProcessPublicGetProductBy(LoadResourceById(container.data_manager, 'product'),
                                                                    container.data_manager),

            # authenticated brand endpoints
            'GET /brands/me': ProcessAuthenticatedGetBrand(container.get_brand_associated_with_cognito_user,
                                                           container.data_manager),

            'POST /brands/me': ProcessAuthenticatedPostBrand(NoBrandAssociatedWithCognitoUser(container.data_manager),
                                                             BrandPostPayloadValidation(), container.data_manager),

            'PUT /brands/me': ProcessAuthenticatedPutBrand(container.get_brand_associated_with_cognito_user,
                                                           BrandPutPayloadValidation(),
                                                           container.data_manager),

            'PATCH /brands/me/image': ProcessAuthenticatedPatchBrandImage(
                                        container.get_brand_associated_with_cognito_user,
                                        BrandImagePatchPayloadValidation(),
                                        update_brand_image,
                                        container.data_manager),

            # authenticated product endpoints
            'GET /products/me': ProcessAuthenticatedGetProducts(container.get_brand_associated_with_cognito_user,
                                                                load_all_products_for_brand_id,
                                                                container.data_manager),

            'GET /products/me/{product_id}': ProcessAuthenticatedGetProductById(
                FilterChainImp([container.get_brand_associated_with_cognito_user, container.valid_product_filter, OwnerOnly('product')]),
                container.data_manager),
            'POST /products/me': ProcessAuthenticatedPostProduct(
                FilterChainImp([container.get_brand_associated_with_cognito_user, ProductPostPayloadValidation()]),
                container.data_manager, container.image_repository, container.status_manager),
            'PUT /products/me/{product_id}': ProcessAuthenticatedPutProduct(
                FilterChainImp(
                    [container.get_brand_associated_with_cognito_user, container.valid_product_filter, OwnerOnly('product'),
                     ProductPutPayloadValidation()]), container.data_manager, container.status_manager),
            'PATCH /products/me/{product_id}/image': ProcessAuthenticatedPatchProductImage(FilterChainImp(
                [container.get_brand_associated_with_cognito_user, container.valid_product_filter, OwnerOnly('product'),
                 ProductImagePatchPayloadValidation()]), container.image_repository, container.data_manager,
                container.status_manager),
            'DELETE /products/me/{product_id}': ProcessAuthenticatedDeleteProduct(
                FilterChainImp([container.get_brand_associated_with_cognito_user, container.valid_product_filter, OwnerOnly('product')]),
                container.data_manager, container.image_repository, container.status_manager),
        })
        print(f'route: {event["routeKey"]}')
        print(f'event: {event}')
        processor: ProcessInterface = routes[event['routeKey']]

        response: PinfluencerResponse = processor.do_process(event)
        if response.is_ok():
            print("finished run processor successfully")
            container.status_manager.status = True
        else:
            print("finished run processor unsuccessfully")
        return response.as_json()

    except KeyError as ke:
        print(f'Missing required key {ke}')
        return PinfluencerResponse.as_400_error().as_json()
    except Exception as e:
        print_exception(e)
        return PinfluencerResponse.as_500_error().as_json()
    finally:
        container.data_manager.cleanup()
