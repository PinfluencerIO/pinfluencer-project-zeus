from src.data_access_layer import to_list
from src.data_access_layer.brand import Brand
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessPublicFeed:
    def __init__(self, load_brands, load_max_3_products_for_brand, data_manager: DataManagerInterface):
        self.load_brands = load_brands
        self.load_max_3_products_for_brand = load_max_3_products_for_brand
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        brands: list[Brand] = self.load_brands(self.data_manager)
        products = []
        for brand in brands:
            products.extend(self.load_max_3_products_for_brand(brand.id, self.data_manager))
        return PinfluencerResponse(body=to_list(products[:20]))
