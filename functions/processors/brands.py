from functions.processors import ProcessInterface
from functions.web.filters import FilterChain
from functions.web.http_util import PinfluencerResponse
from functions.processors.hacks import old_manual_functions


# Todo: Implement these processors


class ProcessPublicBrands(ProcessInterface):
    def __init__(self):
        pass

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        # return PinfluencerResponse(status_code=200, body={'message': 'ProcessPublicBrands'})
        # Todo: Replace the old functions hack with full implementation
        return PinfluencerResponse(status_code=200, body=old_manual_functions.hack_get_brands(event))


class ProcessPublicGetBrandBy(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        # return PinfluencerResponse(status_code=200, body={"message": "ProcessPublicAllProductsForBrand"})
        # Todo: Replace the old functions hack with full implementation
        return PinfluencerResponse(status_code=200, body=old_manual_functions.hack_get_brand_by_id(event))


class ProcessAuthenticatedGetBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        return PinfluencerResponse(status_code=200, body={"message": "ProcessPublicAllProductsForBrand"})


class ProcessAuthenticatedPutBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        return PinfluencerResponse(status_code=200, body={"message": "ProcessAuthenticatedPutBrand"})


class ProcessAuthenticatedPostBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        return PinfluencerResponse(status_code=200, body={"message": "ProcessAuthenticatedPostBrand"})