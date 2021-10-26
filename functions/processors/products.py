from functions.processors import ProcessInterface
from functions.processors.hacks import old_manual_functions
from functions.web.filters import FilterChain, MissingPathParameter, NotFoundById, InvalidId
from functions.web.http_util import PinfluencerResponse


# Todo: Implement all these processors


class ProcessPublicProducts(ProcessInterface):
    def __init__(self):
        pass

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        return old_manual_functions.get_all_products(event)


class ProcessPublicGetProductBy(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return old_manual_functions.get_product_by_id(event)


class ProcessAuthenticatedGetProductById(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return old_manual_functions.get_product_by_id(event)


class ProcessAuthenticatedGetProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return old_manual_functions.hack_product_me(event)


class ProcessAuthenticatedPostProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_chain(event)
        return old_manual_functions.hack_product_me_create(event)


class ProcessAuthenticatedPutProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_chain(event)
        return old_manual_functions.hack_product_me_update(event)

# class ProcessAuthenticatedDeleteProduct(ProcessInterface):
#     def __init__(self, filter_chain: FilterChain):
#         self.filter = filter_chain
#
#     def do_process(self, event: dict) -> PinfluencerResponse:
#         print(self)
#         self.filter.do_filter(event)
#         return old_manual_functions.hack_product_me_delete(event)
