from functions.filters import FilterChainInterface
from functions.http_util import PinfluencerResponse
from functions.processors import ProcessInterface


class ProcessAuthenticatedGetBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChainInterface, service: ResourceServiceInterface):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_filter(event, )
