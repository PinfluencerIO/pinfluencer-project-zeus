from sqlalchemy.orm import Query

from src.data_access_layer.brand import Brand
from src.interfaces.data_manager_interface import DataManagerInterface
from src.web.filters import FilterInterface, BrandAlreadyCreatedForAuthUser, \
    FilterResponse


class AuthFilter(FilterInterface):

    def __init__(self, data_manager: DataManagerInterface):
        self.__data_manager = data_manager

    def do_filter(self, event: dict):
        print('AuthFilter')
        if 'authorizer' in event['requestContext'] \
                and 'authorizer' in event['requestContext'] \
                and 'jwt' in event['requestContext']['authorizer'] \
                and 'claims' in event['requestContext']['authorizer']['jwt'] \
                and 'cognito:username' in event['requestContext']['authorizer']['jwt']['claims']:
            auth_user_id = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']

            print(f'AuthFilter has found the require cognito:username key with {auth_user_id}')
            brand_query: Query = self.__data_manager.session \
                .query(Brand) \
                .filter(Brand.auth_user_id == auth_user_id)
            brand: Brand = brand_query.first()
            if brand is None:
                print(f'Failed to find brand by auth_user_id {auth_user_id}')
                return FilterResponse('Not authorised', 401)
            else:
                event['auth_brand'] = brand.as_dict()
                return FilterResponse('Authorised', 200)
        else:
            print('event was missing the required keys to extract cognito:username')
            return FilterResponse('Not authorised', 401)


class OwnerOnly(FilterInterface):
    def __init__(self, resource):
        self.resource = resource

    def do_filter(self, event: dict):
        print(f'product{event[self.resource]}')
        print(f'auth brand{event["auth_brand"]}')
        if event["product"]['brand']['id'] == event["auth_brand"]['id']:
            return FilterResponse('Authorised', 200)
        else:
            print(f'product {event["product"]["id"]} is not owned by brand {event["auth_brand"]["id"]}')
            return FilterResponse('Not authorised', 401)


class OneTimeCreateBrandFilter(FilterInterface):
    def __init__(self, data_manager: DataManagerInterface):
        self.__data_manager = data_manager

    def do_filter(self, event: dict):
        try:
            auth_user_id = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
        except KeyError:
            return FilterResponse('missing key from event', 400)
        brand_query: Query = self.__data_manager.session \
            .query(Brand) \
            .filter(Brand.auth_user_id == auth_user_id)
        brand: Brand = brand_query.first()
        if brand is None:
            return FilterResponse('', 200)
        else:
            return FilterResponse('Brand already associated with auth user', 400)

