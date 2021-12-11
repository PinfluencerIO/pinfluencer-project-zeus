from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessAuthenticatedPostProduct:
    def __init__(self, get_brand_associated_with_cognito_user,
                 validation,
                 write_new_product,
                 data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.validation = validation
        self.write_new_product = write_new_product
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)

        if filter_response.is_success():
            brand = filter_response.get_payload().as_dict()
            filter_response = self.validation.do_filter(event)
            if filter_response.is_success():
                product = self.write_new_product(filter_response.get_payload(), brand['id'], self.data_manager)
                return PinfluencerResponse(201, product.as_dict())
            else:
                return PinfluencerResponse.as_400_error(filter_response.get_message())
        else:
            return PinfluencerResponse(401, filter_response.get_message())