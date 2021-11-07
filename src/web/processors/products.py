import json

from src.data_access_layer import to_list
from src.data_access_layer.product import Product, product_from_dict
from src.interfaces.data_manager_interface import DataManagerInterface
from src.web.filters import FilterChain
from src.web.http_util import PinfluencerResponse
from src.web.processors import ProcessInterface
from src.web.processors.hacks import old_manual_functions


# Todo: Implement all these processors


class ProcessPublicProducts(ProcessInterface):
    def __init__(self, data_manager: DataManagerInterface):
        super().__init__(data_manager)

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        return PinfluencerResponse(body=to_list(self._data_manager.session.query(Product).all()))


class ProcessPublicGetProductBy(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return PinfluencerResponse(body=event['product'])


class ProcessAuthenticatedGetProductById(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return PinfluencerResponse(body=event["product"])


class ProcessAuthenticatedGetProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        products: list[Product] = (self._data_manager.session
                                   .query(Product)
                                   .filter(Product.brand_id == event["auth_brand"])
                                   .all())
        return PinfluencerResponse(body=to_list(products))


class ProcessAuthenticatedPostProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_chain(event)
        product_dict: dict = json.loads(event['body'])
        product_dict.update({'brand_id': event['auth_brand']['id']})
        product: Product = product_from_dict(product_dict)
        self._data_manager.session.add(product)
        self._data_manager.session.commit()
        return PinfluencerResponse(body=product.as_dict())


class ProcessAuthenticatedPutProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_chain(event)
        return old_manual_functions.update_authenticated_product(event)


class ProcessAuthenticatedDeleteProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain):
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_chain(event)
        return old_manual_functions.delete_authenticated_product(event)


class ProcessAuthenticatedPatchProductImage(ProcessInterface):
    def __init__(self, filter_chain: FilterChain) -> None:
        self.filters = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filters.do_chain(event)
        return old_manual_functions.patch_product_image(event)


class ProcessAuthenticatedPatchBrandImage(ProcessInterface):
    def __init__(self, filter_chain: FilterChain) -> None:
        self.filters = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filters.do_chain(event)
        return old_manual_functions.patch_brand_image(event)
