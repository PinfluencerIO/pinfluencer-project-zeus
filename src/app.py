from src.common.log_util import print_exception
from src.data_access_layer.data_manager import DataManager
from src.web.processors.brands import *
from src.web.processors.feed import *
from src.web.processors.products import *

from src.web.filters import *
from src.web.http_util import PinfluencerResponse
from collections import OrderedDict


def lambda_handler(event, context):
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
        return PinfluencerResponse.as_401_error(e).as_json()
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
        'GET /feed': ProcessPublicFeed(DataManager()),
        'GET /brands': ProcessPublicBrands(DataManager()),
        'GET /brands/{brand_id}': ProcessPublicGetBrandBy(FilterChainImp([ValidBrandId()])),
        'GET /brands/{brand_id}/products': ProcessPublicAllProductsForBrand(FilterChainImp([ValidBrandId()])),
        'GET /products': ProcessPublicProducts(),
        'GET /products/{product_id}': ProcessPublicGetProductBy(FilterChainImp([ValidProductId()])),

        # authenticated brand endpoints
        'GET /brands/me': ProcessAuthenticatedGetBrand(FilterChainImp([(LegacyAuthFilter())])),
        'POST /brands/me': ProcessAuthenticatedPostBrand(
            FilterChainImp([OneTimeCreateBrandFilter(), BrandPostPayloadValidation()])),
        'PUT /brands/me': ProcessAuthenticatedPutBrand(FilterChainImp([LegacyAuthFilter(), BrandPutPayloadValidation()])),
        'PATCH /brands/me/image': ProcessAuthenticatedPatchBrandImage(
            FilterChainImp([LegacyAuthFilter(), BrandImagePatchPayloadValidation()])),

        # authenticated product endpoints
        'GET /products/me': ProcessAuthenticatedGetProduct(FilterChainImp([LegacyAuthFilter()])),
        'GET /products/me/{product_id}': ProcessAuthenticatedGetProductById(
            FilterChainImp([LegacyAuthFilter(), ValidProductId(), OwnerOnly('product')])),
        'POST /products/me': ProcessAuthenticatedPostProduct(
            FilterChainImp([LegacyAuthFilter(), ProductPostPayloadValidation()])),
        'PUT /products/me/{product_id}': ProcessAuthenticatedPutProduct(
            FilterChainImp([LegacyAuthFilter(), ValidProductId(), OwnerOnly('product'), ProductPutPayloadValidation()])),
        'PATCH /products/me/{product_id}/image': ProcessAuthenticatedPatchProductImage(FilterChainImp(
            [LegacyAuthFilter(), ValidProductId(), OwnerOnly('product'), ProductImagePatchPayloadValidation()])),
        'DELETE /products/me/{product_id}': ProcessAuthenticatedDeleteProduct(
            FilterChainImp([LegacyAuthFilter(), ValidProductId(), OwnerOnly('product')])),
    }
)
