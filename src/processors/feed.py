from src.data_access_layer import to_list
from src.data_access_layer.brand import Brand
from src.data_access_layer.read_data_access import load_brands, load_max_3_products_for_brand
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse
from src.processors import ProcessInterface


class ProcessPublicFeed(ProcessInterface):
    def __init__(self, data_manager: DataManagerInterface):
        super().__init__(data_manager)

    def do_process(self, event: dict) -> PinfluencerResponse:
        brands: list[Brand] = load_brands(self._data_manager)
        products = []
        for brand in brands:
            products.extend(load_max_3_products_for_brand(brand.id, self._data_manager))
        return PinfluencerResponse(body=to_list(products[:20]))
