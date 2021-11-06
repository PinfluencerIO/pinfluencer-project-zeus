import json

from src.data_access_layer import to_list
from src.data_access_layer.brand import Brand, brand_from_dict
from src.data_access_layer.product import Product
from src.interfaces.data_manager_interface import DataManagerInterface
from src.web.processors import ProcessInterface, get_user
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
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        brand: Brand = self._data_manager.session.query(Brand)\
            .filter(Brand.id == event['auth_brand']["id"])\
            .first()
        brand_from_body = brand_from_dict(json.loads(event['body']))
        brand.name = brand_from_body.name
        brand.description = brand_from_body.description
        brand.website = brand_from_body.website
        brand.instahandle = brand_from_body.instahandle
        self._data_manager.session.commit()
        return PinfluencerResponse.as_updated(brand.id)


class ProcessAuthenticatedPostBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        brand_dict = json.loads(event['body'])
        brand_dict["auth_user_id"] = get_user(event=event)
        brand = brand_from_dict(brand_dict)
        self._data_manager.session.add(brand)
        self._data_manager.session.commit()
        return PinfluencerResponse.as_created(brand.id)
