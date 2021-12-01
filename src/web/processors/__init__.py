import abc

import boto3

from src.interfaces.data_manager_interface import DataManagerInterface
from src.web.filters import FilterChain, FilterChainImp, FilterResponse
from src.web.http_util import PinfluencerResponse

BUCKET = 'pinfluencer-product-images'

s3 = boto3.client('s3')


# Todo: Not sure this is the right place for an interface...read up about it.
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
