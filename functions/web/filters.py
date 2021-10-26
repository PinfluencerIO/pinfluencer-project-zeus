import abc
import uuid

import schema as schema

from functions import log_util
from functions.processors.hacks.brand_helps import select_brand_by_id, select_brand_by_auth_user_id
from functions.processors.hacks.product_helps import select_product_by_id


class MissingPathParameter(Exception):
    pass


class NotFoundById(Exception):
    pass


class InvalidId(Exception):
    pass


class FilterChain:
    @abc.abstractmethod
    def do_chain(self, event):
        pass


class FilterInterface:
    @abc.abstractmethod
    def do_filter(self, event: dict):
        pass


class FilterChainImp(FilterChain):
    """
    Handles the chaining of calls through the FilterChain
    """

    def __init__(self, filters: list[FilterInterface]):
        self.filters = filters

    def do_chain(self, event: dict):
        for filter_ in self.filters:
            filter_.do_filter(event)


class ValidBrandId(FilterInterface):
    def __init__(self):
        pass

    def do_filter(self, event: dict):
        try:
            id_ = event['pathParameters']['brand_id']
        except KeyError as key_error:
            raise MissingPathParameter(f'Required brand_id in path parameters in event: {key_error}')

        if valid_uuid(id_):
            try:
                list_of_brands = select_brand_by_id(id_)
            except Exception as e:
                print(f'Failed db call get brand by id {id_}')
                raise e

            if len(list_of_brands) == 0:
                raise NotFoundById(f'Failed to find brand by id {id_}')
            else:
                event['brand'] = list_of_brands[0]
        else:
            raise InvalidId(f'Invalid id {id_} in path for brand')


class ValidProductId(FilterInterface):
    def __init__(self):
        pass

    def do_filter(self, event: dict):
        try:
            id_ = event['pathParameters']['product_id']
        except KeyError as key_error:
            print(f'Required product_id in path parameters in event: {key_error}')
            raise key_error

        if valid_uuid(id_):
            print('valid product id in path')
            try:
                list_of_products = select_product_by_id(id_)
            except Exception as e:
                print(f'Failed db call get product by id {id_}')
                raise e

            if len(list_of_products) == 0:
                raise NotFoundById(f'Failed to find product by id {id_}')
            else:
                event['product'] = list_of_products[0]
        else:
            raise InvalidId(f'Invalid id {id_} in path for product')


def valid_uuid(id_):
    try:
        val = uuid.UUID(id_, version=4)
        # If uuid_string is valid hex, but invalid uuid4, UUID.__init__ converts to valid uuid4.
        # This is bad for validation purposes, so try and match str with UUID
        if str(val) == id_:
            return True
        else:
            log_util.print_exception(f'equality failed {val} {id_}')
    except ValueError as ve:
        log_util.print_exception(ve)
    except AttributeError as e:
        log_util.print_exception(e)

    return False


class AuthFilter(FilterInterface):
    """
    Todo: Implement this filter
    Get cognito:username from authorizer and puts it in top level event dictionary.
    """

    def do_filter(self, event: dict):
        print('AuthFilter')
        if 'authorizer' in event['requestContext'] \
                and 'authorizer' in event['requestContext'] \
                and 'jwt' in event['requestContext']['authorizer'] \
                and 'claims' in event['requestContext']['authorizer']['jwt'] \
                and 'cognito:username' in event['requestContext']['authorizer']['jwt']['claims']:
            auth_user_id = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
            print(f'AuthFilter has found the require cognito:username key with {auth_user_id}')
            try:
                list_of_brands = select_brand_by_auth_user_id(auth_user_id)
                if len(list_of_brands) == 0:
                    raise NotFoundById(f'Failed to find brand by auth_user_id {auth_user_id}')
                else:
                    event['auth_brand'] = list_of_brands[0]
            except Exception as e:
                print(f'Failed db call get brand by auth_user_id {auth_user_id}')
                raise e
        else:
            # Todo: this needs to be handled via an exception and remove filter.chain call
            print(f'event was missing the required keys to extract cognito:username')
