from src.common.log_util import print_exception
from src.data_access_layer.data_manager import DataManager
from src.services import Container
from src.web.processors.brands import *
from src.web.processors.feed import *
from src.web.processors.products import *

from src.web.filters import *
from src.web.http_util import PinfluencerResponse
from collections import OrderedDict

container: Container = Container()


def lambda_handler(event, context):
    global container
    container = Container()
    try:
        print(f'route: {event["routeKey"]}')
        print(f'event: {event}')
        return routes[event['routeKey']].do_process(event).as_json()
    except KeyError as ke:
        print(f'Missing required key {ke}')
        return PinfluencerResponse.as_400_error().as_json()
    except NotFoundById:
        print(f'NotFoundById')
        return PinfluencerResponse.as_404_error().as_json()
    except NotFoundByAuthUser as e:
        print(f'NotFoundByAuthUser')
        return PinfluencerResponse.as_401_error(str(e)).as_json()
    except OwnershipError as ownership:
        return PinfluencerResponse.as_401_error(str(ownership)).as_json()
    except InvalidId:
        print(f'InvalidId')
        return PinfluencerResponse.as_400_error().as_json()
    except PayloadValidationError:
        print(f'BrandPayloadValidationError')
        return PinfluencerResponse.as_400_error().as_json()
    except BrandAlreadyCreatedForAuthUser:
        print(f'BrandAlreadyCreatedForAuthUser')
        return PinfluencerResponse.as_400_error('There is already a brand associated with this auth user').as_json()
    except Exception as e:
        print_exception(e)
        return PinfluencerResponse.as_500_error().as_json()


routes = OrderedDict(
    {
        # public endpoints
        'GET /feed': ProcessPublicFeed(container.data_manager),
        'GET /brands': ProcessPublicBrands(container.data_manager),
        'GET /brands/{brand_id}': ProcessPublicGetBrandBy(FilterChainImp([ValidBrandId()]), container.data_manager),
        'GET /brands/{brand_id}/products': ProcessPublicAllProductsForBrand(FilterChainImp([ValidBrandId()]),
                                                                            container.data_manager),
        'GET /products': ProcessPublicProducts(),
        'GET /products/{product_id}': ProcessPublicGetProductBy(FilterChainImp([ValidProductId()])),

        # authenticated brand endpoints
        'GET /brands/me': ProcessAuthenticatedGetBrand(FilterChainImp([container.auth_filter]), container.data_manager),
        'POST /brands/me': ProcessAuthenticatedPostBrand(
            FilterChainImp([OneTimeCreateBrandFilter(container.data_manager), BrandPostPayloadValidation()])),
        'PUT /brands/me': ProcessAuthenticatedPutBrand(FilterChainImp([container.auth_filter, BrandPutPayloadValidation()])),
        'PATCH /brands/me/image': ProcessAuthenticatedPatchBrandImage(
            FilterChainImp([container.auth_filter, BrandImagePatchPayloadValidation()])),

        # authenticated product endpoints
        'GET /products/me': ProcessAuthenticatedGetProduct(FilterChainImp([container.auth_filter])),
        'GET /products/me/{product_id}': ProcessAuthenticatedGetProductById(
            FilterChainImp([container.auth_filter, ValidProductId(), OwnerOnly('product')])),
        'POST /products/me': ProcessAuthenticatedPostProduct(
            FilterChainImp([container.auth_filter, ProductPostPayloadValidation()])),
        'PUT /products/me/{product_id}': ProcessAuthenticatedPutProduct(
            FilterChainImp([container.auth_filter, ValidProductId(), OwnerOnly('product'), ProductPutPayloadValidation()])),
        'PATCH /products/me/{product_id}/image': ProcessAuthenticatedPatchProductImage(FilterChainImp(
            [container.auth_filter, ValidProductId(), OwnerOnly('product'), ProductImagePatchPayloadValidation()])),
        'DELETE /products/me/{product_id}': ProcessAuthenticatedDeleteProduct(
            FilterChainImp([container.auth_filter, ValidProductId(), OwnerOnly('product')])),
    }
)
