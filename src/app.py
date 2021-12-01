from collections import OrderedDict

from src.common.log_util import print_exception
from src.container import Container
from src.web.filters import *
from src.web.filters.authorised_filter import *
from src.web.filters.payload_validation import *
from src.web.processors.brands import *
from src.web.processors.feed import *
from src.web.processors.products import *


def lambda_handler(event, context):
    container = Container()
    try:
        routes = OrderedDict({
            # public endpoints
            'GET /feed': ProcessPublicFeed(container.data_manager),
            'GET /brands': ProcessPublicBrands(container.data_manager),
            'GET /brands/{brand_id}': ProcessPublicGetBrandBy(FilterChainImp([container.valid_brand_filter]),
                                                              container.data_manager),
            'GET /brands/{brand_id}/products': ProcessPublicAllProductsForBrand(
                FilterChainImp([container.valid_brand_filter]),
                container.data_manager),
            'GET /products': ProcessPublicProducts(container.data_manager),
            'GET /products/{product_id}': ProcessPublicGetProductBy(
                FilterChainImp([container.valid_product_filter]),
                container.data_manager),

            # authenticated brand endpoints
            'GET /brands/me': ProcessAuthenticatedGetBrand(FilterChainImp([container.auth_filter]),
                                                           container.data_manager),
            'POST /brands/me': ProcessAuthenticatedPostBrand(
                FilterChainImp([OneTimeCreateBrandFilter(container.data_manager),
                                BrandPostPayloadValidation()]),
                container.data_manager, container.image_repository, container.status_manager),
            'PUT /brands/me': ProcessAuthenticatedPutBrand(FilterChainImp([container.auth_filter,
                                                                           BrandPutPayloadValidation()]),
                                                           container.data_manager, container.status_manager),
            'PATCH /brands/me/image': ProcessAuthenticatedPatchBrandImage(
                FilterChainImp([container.auth_filter, BrandImagePatchPayloadValidation()]),
                container.data_manager,
                container.image_repository, container.status_manager),

            # authenticated product endpoints
            'GET /products/me': ProcessAuthenticatedGetProduct(FilterChainImp([container.auth_filter]),
                                                               container.data_manager),
            'GET /products/me/{product_id}': ProcessAuthenticatedGetProductById(
                FilterChainImp([container.auth_filter, container.valid_product_filter, OwnerOnly('product')]),
                container.data_manager),
            'POST /products/me': ProcessAuthenticatedPostProduct(
                FilterChainImp([container.auth_filter, ProductPostPayloadValidation()]),
                container.data_manager, container.image_repository, container.status_manager),
            'PUT /products/me/{product_id}': ProcessAuthenticatedPutProduct(
                FilterChainImp(
                    [container.auth_filter, container.valid_product_filter, OwnerOnly('product'),
                     ProductPutPayloadValidation()]), container.data_manager, container.status_manager),
            'PATCH /products/me/{product_id}/image': ProcessAuthenticatedPatchProductImage(FilterChainImp(
                [container.auth_filter, container.valid_product_filter, OwnerOnly('product'),
                 ProductImagePatchPayloadValidation()]), container.image_repository, container.data_manager,
                container.status_manager),
            'DELETE /products/me/{product_id}': ProcessAuthenticatedDeleteProduct(
                FilterChainImp([container.auth_filter, container.valid_product_filter, OwnerOnly('product')]),
                container.data_manager, container.image_repository, container.status_manager),
        })
        print(f'route: {event["routeKey"]}')
        print(f'event: {event}')
        processor: ProcessInterface = routes[event['routeKey']]
        print("start run filters")
        filter_response: FilterResponse = processor.run_filters(event)

        if filter_response.is_success():
            print("finished run filters successfully")
            print("start run processor")
            response: PinfluencerResponse = processor.do_process(event)
            if response.is_ok():
                print("finished run processor successfully")
                container.status_manager.status = True
            else:
                print("finished run processor unsuccessfully")
            return response.as_json()
        else:
            print("finished run filters unsuccessfully")
            container.status_manager.status = True
            return PinfluencerResponse(filter_response.get_code(), filter_response.get_message())

    except KeyError as ke:
        print(f'Missing required key {ke}')
        return PinfluencerResponse.as_400_error().as_json()
    except Exception as e:
        print_exception(e)
        return PinfluencerResponse.as_500_error().as_json()
    finally:
        container.data_manager.cleanup()
