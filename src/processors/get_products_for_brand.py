from src.data_access_layer import to_list
from src.filters.valid_id_filters import LoadResourceById
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessPublicAllProductsForBrand:
    def __init__(self, load_resource_by_id: LoadResourceById, load_all_products_for_brand_id,
                 data_manager: DataManagerInterface):
        self.load_resource_by_id = load_resource_by_id
        self.load_all_products_for_brand_id = load_all_products_for_brand_id
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        response = self.load_resource_by_id.load(event)
        if response.is_success():
            brand = response.get_payload()
            products_for_brand = self.load_all_products_for_brand_id(brand['id'], self.data_manager)
            return PinfluencerResponse(body=(to_list(products_for_brand)))
        else:
            return PinfluencerResponse.as_400_error(response.get_message())