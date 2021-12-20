from src.data_access_layer import to_list
from src.pinfluencer_response import PinfluencerResponse
from src.processors import valid_path_resource_id


class ProcessGetProductsForBrand:
    def __init__(self, load_all_products_for_brand_id, data_manager):
        self.load_all_products_for_brand_id = load_all_products_for_brand_id
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        brand_id = valid_path_resource_id(event, 'brand_id')
        if brand_id:
            products_for_brand = self.load_all_products_for_brand_id(brand_id, self.data_manager)
            if products_for_brand:
                return PinfluencerResponse(body=(to_list(products_for_brand)))
            else:
                return PinfluencerResponse(404, "Not found")
        else:
            return PinfluencerResponse.as_400_error(f'{self} Invalid path parameter id')

