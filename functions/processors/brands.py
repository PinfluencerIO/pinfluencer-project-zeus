from functions.processors import ProcessInterface
from functions.web.filters import FilterChain, MissingPathParameter, NotFoundById, InvalidId
from functions.web.http_util import PinfluencerResponse
from functions.processors.hacks import old_manual_functions


# Todo: Implement these processors


class ProcessPublicBrands(ProcessInterface):
    def __init__(self):
        pass

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        return old_manual_functions.get_all_brands(event)


class ProcessPublicGetBrandBy(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filters = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filters.do_chain(event)
        return old_manual_functions.get_brand_by_id(event)


class ProcessPublicAllProductsForBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return old_manual_functions.get_all_products_for_brand_with_id(event)

#
# class ProcessAuthenticatedGetBrand(ProcessInterface):
#     def __init__(self, filter_chain: FilterChain):
#         self.filter = filter_chain
#
#     def do_process(self, event: dict) -> PinfluencerResponse:
#         print(self)
#         self.filter.do_filter(event)
#         # Todo: Replace the old functions hack with full implementation
#         return old_manual_functions.hack_brand_me(event)
#
#
# class ProcessAuthenticatedPutBrand(ProcessInterface):
#     def __init__(self, filter_chain: FilterChain):
#         self.filter = filter_chain
#
#     def do_process(self, event: dict) -> PinfluencerResponse:
#         print(self)
#         self.filter.do_filter(event)
#         # Todo: Replace the old functions hack with full implementation
#         return old_manual_functions.hack_brand_me_update(event)
#
#
# class ProcessAuthenticatedPostBrand(ProcessInterface):
#     def __init__(self, filter_chain: FilterChain):
#         self.filter = filter_chain
#
#     def do_process(self, event: dict) -> PinfluencerResponse:
#         print(self)
#         self.filter.do_filter(event)
#         # Todo: Replace the old functions hack with full implementation
#         return old_manual_functions.hack_brand_me_create(event)
