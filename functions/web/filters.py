import abc
import uuid

import schema as schema

from functions import log_util


class FilterChain:
    @abc.abstractmethod
    def do_filter(self, event: dict):
        pass


class FilterInterface:
    @abc.abstractmethod
    def do_filter(self, event: dict, filter_chain: FilterChain):
        pass


class FilterChainImp(FilterChain):
    """
    Handles the chaining of calls through the FilterChain
    """

    def __init__(self, filters: list[FilterInterface]):
        self.filter_iterator = iter(filters)

    def do_filter(self, event: dict):
        try:
            next(self.filter_iterator).do_filter(event, self)
        except Exception as e:
            print(e)
            pass


class AuthFilter(FilterInterface):
    """
    Todo: Implement this filter
    Get cognito:username from authorizer and puts it in top level event dictionary.
    """

    def do_filter(self, event: dict, filter_chain: FilterChain):
        print('AuthFilter')
        if 'authorizer' in event['requestContext'] \
                and 'authorizer' in event['requestContext'] \
                and 'jwt' in event['requestContext']['authorizer'] \
                and 'claims' in event['requestContext']['authorizer']['jwt'] \
                and 'cognito:username' in event['requestContext']['authorizer']['jwt']['claims']:
            id_ = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
            print(f'AuthFilter has found the require cognito:username key with {id_}')
            filter_chain.do_filter(event)
        else:
            # Todo: this needs to be handled via an exception and remove filter.chain call
            print(f'event was missing the required keys to extract cognito:username')
            filter_chain.do_filter(event)


class PayloadFilter(FilterInterface):
    """
    Todo: Implement this filter to extract and validate the payload against schema
    """
    def __init__(self, schema_: schema):
        self.schema = schema_

    def do_filter(self, event: dict, filter_chain: FilterChain):
        print('PayloadFilter')
        filter_chain.do_filter(event)


class ValidId(FilterInterface):
    """
    Todo: Implement this filter to...
    Get path parameter from event, and validates it is a UUID.
    """

    def __init__(self, parameter_name: str):
        self.parameter_name = parameter_name

    def do_filter(self, event: dict, filter_chain: FilterChain):
        print('ValidIdFilter')

        if 'pathParameters' in event \
                and self.parameter_name in event['pathParameters'] \
                and self.valid_uuid(event['pathParameters'][self.parameter_name]):
            id_ = event['pathParameters'][self.parameter_name]
            print(f'ValidIdFilter has found and validated PathParameter {self.parameter_name} as {id_}')
            filter_chain.do_filter(event)
        else:
            print('missing id or invalid')
            raise Exception('invalid id')

    def valid_uuid(self, id_):
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
