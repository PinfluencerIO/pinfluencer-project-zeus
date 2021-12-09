import abc

import boto3

from src.interfaces.data_manager_interface import DataManagerInterface
from src.filters import FilterChain, FilterChainImp, FilterResponse
from src.pinfluencer_response import PinfluencerResponse

BUCKET = 'pinfluencer-product-images'

s3 = boto3.client('s3')


class ProcessInterface(abc.ABC):
    _data_manager: DataManagerInterface

    def __init__(self,
                 data_manager: DataManagerInterface,
                 filters: FilterChain = FilterChainImp([])):
        self._data_manager = data_manager
        self.__filters = filters

    @abc.abstractmethod
    def do_process(self, event: dict) -> PinfluencerResponse:
        pass

    def run_filters(self, event: dict) -> FilterResponse:
        return self.__filters.do_chain(event=event)


def get_user(event):
    return event['requestContext']['authorizer']['jwt']['claims']['cognito:username']


def protect_email_from_update_if_held_in_claims(body, event):
    if ('email' in event['requestContext']['authorizer']['jwt']['claims'] and
            event['requestContext']['authorizer']['jwt']['claims']['email'] is not None):
        print(f"Found email in claim: {event['requestContext']['authorizer']['jwt']['claims']['email']}")
        print(f'before {body}')
        body['email'] = event['requestContext']['authorizer']['jwt']['claims']['email']
        print(f'after {body}')