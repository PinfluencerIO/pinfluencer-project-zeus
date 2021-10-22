from functions.processors.brands import *
from functions.processors.feed import ProcessPublicFeed
from functions.processors.products import *

from functions.web.filters import FilterChainImp, ValidId, AuthFilter, PayloadFilter
from functions.web.http_util import PinfluencerResponse
from collections import OrderedDict


def lambda_handler(event, context):
    if 'routeKey' in event and event['routeKey'] in routes:
        print(event['routeKey'])
        return routes[event['routeKey']].do_process(event).format()
    else:
        return PinfluencerResponse(400, {}).format()


routes = OrderedDict(
    {
        # public endpoints
        'GET /feed': ProcessPublicFeed(),
        'GET /brands': ProcessPublicBrands(),
        'GET /brands/<brand_id>': ProcessPublicGetBrandBy(FilterChainImp([ValidId('brand_id')])),
        'GET /brands/<brand_id>/products': ProcessPublicAllProductsForBrand(FilterChainImp([ValidId('brand_id')])),
        'GET /products': ProcessPublicProducts(),
        'GET /products/<product_id>': ProcessPublicGetProductBy(FilterChainImp([ValidId('product_id')])),

        # authenticated brand endpoints
        'GET /brands/me': ProcessAuthenticatedGetBrand(FilterChainImp([(AuthFilter())])),
        'POST /brands/me': ProcessAuthenticatedPostBrand(FilterChainImp([AuthFilter(), PayloadFilter(None)])),
        'PUT /brands/me': ProcessAuthenticatedPutBrand(FilterChainImp([AuthFilter(), PayloadFilter(None)])),

        # authenticated product endpoints
        'GET /products/me': ProcessAuthenticatedGetProduct(FilterChainImp([(AuthFilter())])),
        'POST /products/me': ProcessAuthenticatedPostProduct(FilterChainImp([AuthFilter(), PayloadFilter(None)])),
        'PUT /products/me/<product_id>': ProcessAuthenticatedPutProduct(
            FilterChainImp([AuthFilter(), ValidId('product_id'), PayloadFilter(None)])),
        'DELETE /products/me/<product_id>': ProcessAuthenticatedDeleteProduct(
            FilterChainImp([AuthFilter(), ValidId('product_id')])),
    }
)
