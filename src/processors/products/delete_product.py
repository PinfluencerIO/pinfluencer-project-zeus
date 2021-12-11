from src.filters.valid_id_filters import valid_uuid
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessAuthenticatedDeleteProduct:
    def __init__(self, get_brand_associated_with_cognito_user,
                 delete_product, data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.delete_product = delete_product
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)
        if filter_response.is_success():
            product_id = event['pathParameters']['product_id']
            brand_id = filter_response.get_payload().as_dict()['id']
            if valid_uuid(product_id):
                product = self.delete_product(brand_id, product_id, self.data_manager)
                if product:
                    return PinfluencerResponse(200, f"{product} deleted")
                else:
                    return PinfluencerResponse(404, "Not found")
            else:
                return PinfluencerResponse.as_400_error(filter_response.get_message())
        else:
            return PinfluencerResponse(401, filter_response.get_message())