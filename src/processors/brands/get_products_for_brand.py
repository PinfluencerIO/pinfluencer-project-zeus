from src.data_access_layer import to_list
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse
from src.processors import valid_path_resource_id


class ProcessPublicAllProductsForBrand:
    def __init__(self, load_all_products_for_brand_id,
                 data_manager: DataManagerInterface):
        self.load_all_products_for_brand_id = load_all_products_for_brand_id
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        id_ = valid_path_resource_id(event, 'brand_id')
        if id_:
            products_for_brand = self.load_all_products_for_brand_id(id_, self.data_manager)
            if products_for_brand:
                return PinfluencerResponse(body=(to_list(products_for_brand)))
            else:
                return PinfluencerResponse(404, "Not found")
        else:
            return PinfluencerResponse.as_400_error('Invalid path parameter id')

