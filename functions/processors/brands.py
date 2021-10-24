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
        # Todo: Replace the old functions hack with full implementation
        return PinfluencerResponse(status_code=200, body=old_manual_functions.hack_get_brands(event))


class ProcessPublicGetBrandBy(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        # Todo: Replace the old functions hack with full implementation
        return PinfluencerResponse(status_code=200, body=old_manual_functions.hack_get_brand_by_id(event))


class ProcessAuthenticatedGetBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        # Todo: Replace the old functions hack with full implementation
        me = old_manual_functions.hack_brand_me(event)
        if len(me) == 0:
            return PinfluencerResponse(status_code=404, body={})
        else:
            return PinfluencerResponse(status_code=200, body=me)


class ProcessAuthenticatedPutBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        # Todo: Replace the old functions hack with full implementation
        return PinfluencerResponse(status_code=200, body=old_manual_functions.hack_brand_me_update(event))


class ProcessAuthenticatedPostBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        # Todo: Replace the old functions hack with full implementation
        return PinfluencerResponse(status_code=201, body=old_manual_functions.hack_brand_me_create(event))
