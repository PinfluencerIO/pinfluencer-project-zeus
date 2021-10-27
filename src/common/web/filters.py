import abc
import json
import uuid

from jsonschema import validate

from src.crosscutting import log_util
from src.processors.hacks.brand_helps import select_brand_by_id, select_brand_by_auth_user_id
from src.processors.hacks.product_helps import select_product_by_id


class MissingPathParameter(Exception):
    pass


class NotFoundById(Exception):
    pass


class NotFoundByAuthUser(Exception):
    pass


class InvalidId(Exception):
    pass


class PayloadValidationError(Exception):
    pass


class BrandAlreadyCreatedForAuthUser(Exception):
    pass


class OwnershipError(Exception):
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


class OneTimeCreateBrandFilter(FilterInterface):
    def do_filter(self, event: dict):
        try:
            AuthFilter().do_filter(event)
        except NotFoundByAuthUser:
            print(f'No brand associated auth user id; continue')
            return

        raise BrandAlreadyCreatedForAuthUser(f'brand already associated with auth user')


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
            list_of_brands = select_brand_by_auth_user_id(auth_user_id)
            if len(list_of_brands) == 0:
                raise NotFoundByAuthUser(f'Failed to find brand by auth_user_id {auth_user_id}')
            else:
                event['auth_brand'] = list_of_brands[0]
        else:
            # Todo: this needs to be handled via an exception and remove filter.chain call
            print(f'event was missing the required keys to extract cognito:username')


def get_product_payload_schema():
    schema = {
        "type": "object",
        "properties":
            {
                "name": {
                    "type": "string",
                    "pattern": "^.{1,120}$"
                },
                "description": {
                    "type": "string",
                    "pattern": "^.{1,500}$"
                },
                "requirements": {
                    "type": "string",
                    "pattern": "^.{1,500}$"
                },
                "image": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "pattern": "^.{1,120}$"
                        },
                        "bytes": {
                            "type": "string"
                        }
                    }
                }
            },
        "required": ["name", "description", "requirements", "image"]
    }
    return schema


def get_brand_payload_schema():
    schema = {
        "type": "object",
        "properties":
            {
                "name": {
                    "type": "string",
                    "pattern": "^.{1,120}$"
                },
                "description": {
                    "type": "string",
                    "pattern": "^.{1,500}$"
                },
                "website": {
                    "type": "string",
                    "pattern": "^(https?\:\/\/)?([\da-zA-Z\.-]+)\.([a-z\.]{2,6})(\/[\w]*)*$"
                },
                "email": {
                    "type": "string",
                    "pattern": "^[a-zA-Z0-9\._-]+[@]{1}[a-zA-Z0-9\._-]+[\.]+[a-zA-Z0-9]+$"
                },
                "image": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "pattern": "^.{1,120}$"
                        },
                        "bytes": {
                            "type": "string"
                        }
                    }
                }
            },
        "required": ["name", "description", "website", "email", "image"]
    }
    return schema


class ProductPostPayloadValidation(FilterInterface):
    def do_filter(self, event: dict):
        body_ = event["body"]
        payload = json.loads(body_)
        print(f'payload {payload}')
        try:
            validate(instance=payload, schema=(get_product_payload_schema()))
        except Exception as e:
            print(f'Validating product payload failed {e}')
            raise PayloadValidationError(f'Validating product payload failed {e}')

        print(f'Validate brand create payload {body_}')
        pass


class BrandPostPayloadValidation(FilterInterface):
    def do_filter(self, event: dict):
        body_ = event["body"]
        payload = json.loads(body_)
        print(f'payload {payload}')
        try:
            validate(instance=payload, schema=(get_brand_payload_schema()))
            if len(payload['email']) > 120:
                print(f'email is longer than column size, clipping ')
                payload['email'] = payload['email'][:120]
            if len(payload['website']) > 120:
                print(f'website is longer than column size, clipping ')
                payload['website'] = payload['website'][:120]
        except Exception as e:
            print(f'Validating brand payload failed {e}')
            raise PayloadValidationError()

        print(f'Validate brand create payload {body_}')
        pass


class OwnerOnly(FilterInterface):
    def __init__(self, resource):
        self.resource = resource

    def do_filter(self, event: dict):
        print(f'product{event[self.resource]}')
        print(f'auth brand{event["auth_brand"]}')
        if event["product"]['brand']['id'] == event["auth_brand"]['id']:
            pass
        else:
            raise OwnershipError(f'product {event["product"]["id"]} is not owned by brand {event["auth_brand"]["id"]}')
