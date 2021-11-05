from src.data_access_layer import to_list
from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.interfaces.data_manager_interface import DataManagerInterface
from src.web.processors import ProcessInterface
from src.web.filters import FilterChain
from src.web.http_util import PinfluencerResponse
from src.web.processors.hacks import old_manual_functions


# Todo: Implement these processors


class ProcessPublicBrands(ProcessInterface):
    def __init__(self, data_manager: DataManagerInterface):
        super().__init__(data_manager)

    def do_process(self, event: dict) -> PinfluencerResponse:
        return PinfluencerResponse(body=to_list(self._data_manager.session
                                                .query(Brand)
                                                .all()))


class ProcessPublicGetBrandBy(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filters = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filters.do_chain(event)
        return PinfluencerResponse(body=to_list(self._data_manager.session
                                                .query(Brand)
                                                .filter(Brand.id == event['brand']['id'])
                                                .first()))


class ProcessPublicAllProductsForBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return PinfluencerResponse(body=to_list(self._data_manager.session
                                                .query(Product)
                                                .filter(Product.brand_id == event['brand']['id'])
                                                .first()))


class ProcessAuthenticatedGetBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        print(f'found auth brand {event["auth_brand"]}')
        return PinfluencerResponse(body=event["auth_brand"])


class ProcessAuthenticatedPutBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return old_manual_functions.update_authenticated_brand(event)


class ProcessAuthenticatedPostBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return old_manual_functions.create_authenticated_brand(event)
