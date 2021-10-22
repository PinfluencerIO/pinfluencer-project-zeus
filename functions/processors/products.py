from functions.processors import ProcessInterface
from functions.web.filters import FilterChain
from functions.web.http_util import PinfluencerResponse

# Todo: Implement these processors


class ProcessPublicAllProductsForBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        return PinfluencerResponse(status_code=200, body={"message": "ProcessPublicAllProductsForBrand"})


class ProcessPublicProducts(ProcessInterface):
    def __init__(self):
        pass

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        return PinfluencerResponse(status_code=200, body={"message": "ProcessPublicProducts"})


class ProcessPublicGetProductBy(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        return PinfluencerResponse(status_code=200, body={"message": "ProcessPublicGetProductBy"})


class ProcessAuthenticatedGetProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        return PinfluencerResponse(status_code=200, body={"message": "ProcessAuthenticatedGetProduct"})


class ProcessAuthenticatedPostProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        return PinfluencerResponse(status_code=200, body={"message": "ProcessAuthenticatedPostProduct"})


class ProcessAuthenticatedPutProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        return PinfluencerResponse(status_code=200, body={"message": "ProcessAuthenticatedPutProduct"})


class ProcessAuthenticatedDeleteProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        return PinfluencerResponse(status_code=200, body={"message": "ProcessAuthenticatedDeleteProduct"})