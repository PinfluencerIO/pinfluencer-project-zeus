from functions.processors import ProcessInterface
from functions.processors.hacks import old_manual_functions
from functions.web.filters import FilterChain
from functions.web.http_util import PinfluencerResponse


# Todo: Implement these processors


class ProcessPublicAllProductsForBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        # return PinfluencerResponse(status_code=200, body={"message": "ProcessPublicAllProductsForBrand"})
        return PinfluencerResponse(status_code=200,
                                   body=old_manual_functions.hack_get_all_products_for_brand_by_id(event))


class ProcessPublicProducts(ProcessInterface):
    def __init__(self):
        pass

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        # return PinfluencerResponse(status_code=200, body={"message": "ProcessPublicProducts"})
        return PinfluencerResponse(status_code=200, body=old_manual_functions.hack_get_products(event))


class ProcessPublicGetProductBy(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        # return PinfluencerResponse(status_code=200, body={"message": "ProcessPublicGetProductBy"})
        return PinfluencerResponse(status_code=200, body=old_manual_functions.hack_get_product_by_id(event))


class ProcessAuthenticatedGetProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        # return PinfluencerResponse(status_code=200, body={"message": "ProcessAuthenticatedGetProduct"})
        # Todo: Replace the old functions hack with full implementation
        return PinfluencerResponse(status_code=200, body=old_manual_functions.hack_product_me(event))


class ProcessAuthenticatedPostProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_filter(event)
        return PinfluencerResponse(status_code=200, body=old_manual_functions.hack_product_me_create(event))


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
