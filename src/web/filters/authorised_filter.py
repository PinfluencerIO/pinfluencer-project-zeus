from src.interfaces.data_manager_interface import DataManagerInterface
from src.service_layer import load_brand_by_auth_id
from src.web.filters import FilterInterface, FilterResponse


class AuthFilter(FilterInterface):

    def __init__(self, data_manager: DataManagerInterface):
        self.__data_manager = data_manager

    def do_filter(self, event: dict):
        print('AuthFilter')
        try:
            auth_user_id = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
        except KeyError:
            print('event was missing the required keys to extract cognito:username')
            return FilterResponse('Missing username in event', 401)

        print(f'AuthFilter has found the require cognito:username key with {auth_user_id}')

        loaded_brand = load_brand_by_auth_id(auth_user_id, self.__data_manager)

        if loaded_brand is None:
            print(f'Failed to find brand by auth_user_id {auth_user_id}')
            return FilterResponse('Not authorised', 401)
        else:
            event['auth_brand'] = loaded_brand.as_dict()
            return FilterResponse('Authorised', 200)


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
        loaded_brand = load_brand_by_auth_id(auth_user_id, self.__data_manager)
        if loaded_brand is None:
            return FilterResponse('No brand associated with user', 200)
        else:
            return FilterResponse('Brand already associated with user', 400)
