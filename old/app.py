from filters import FilterChainImp
from functions import http_util
from functions.web.brand_controller import GetMeBrand

from collections import OrderedDict

from functions.filters import AuthFilter


def lambda_handler(event, context):
    if 'routeKey' in event and event['routeKey'] in routes:
        return routes[event['routeKey']].do_process(event).format()
    else:
        return http_util.PinfluencerResponse(400, {}).format()


def extract_payload(event):
    return None if 'body' not in event else event['body']


routes = OrderedDict(
    {
        # 'GET /feed': p,
        # 'GET /brands': p,
        # 'GET /brands/<brand_id>': p,
        # 'GET /brands/<brand_id>/products': p,
        # 'GET /products': p,
        # 'GET /products/<product_id>': p,

        'GET /brands/me': (GetMeBrand(FilterChainImp([(AuthFilter())]), None)),
        # 'POST /brands/me': extract_auth,
        # 'PUT /brands/me': extract_auth,

        # 'GET /products/me': p,
        # 'POST /products/me': p,
        # 'PUT /products/me/<product_id>': p,
        # 'DELETE /products/me/<product_id>': p,
    }
)
