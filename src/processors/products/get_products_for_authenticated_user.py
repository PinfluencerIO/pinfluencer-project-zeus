from src.data_access_layer import to_list
from src.data_access_layer.product import Product
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessAuthenticatedGetProducts:
    def __init__(self, get_brand_associated_with_cognito_user,
                 load_all_products_for_brand_id,
                 data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.load_all_products_for_brand_id = load_all_products_for_brand_id
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)

        if filter_response.is_success():
            brand = filter_response.get_payload().as_dict()
            products: list[Product] = self.load_all_products_for_brand_id(
                brand['id'],
                self.data_manager)
            return PinfluencerResponse(body=to_list(products))
        else:
            return PinfluencerResponse(401, filter_response.get_message())