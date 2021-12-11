from src.filters.valid_id_filters import valid_uuid
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessPublicGetProductBy:
    def __init__(self, load_resource_by_id, data_manager: DataManagerInterface):
        self.load_resource_by_id = load_resource_by_id
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        response = self.load_resource_by_id.do_filter(event)
        if response.is_success():
            return PinfluencerResponse(body=response.get_payload())
        else:
            return PinfluencerResponse(response.get_code(), response.get_message())


class ProcessAuthenticatedGetProductById:
    def __init__(self, get_brand_associated_with_cognito_user, load_product_by_id_owned_by_brand,
                 data_manager: DataManagerInterface):
        self.data_manager = data_manager
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.load_product_by_id_owned_by_brand = load_product_by_id_owned_by_brand

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)
        if filter_response.is_success():
            brand = filter_response.get_payload().as_dict()
            product_id = event['pathParameters']['product_id']
            if valid_uuid(product_id):
                product = self.load_product_by_id_owned_by_brand(product_id, brand,
                                                                 self.data_manager)
                if product:
                    return PinfluencerResponse(200, product.as_dict())
                else:
                    return PinfluencerResponse(404, 'Not found')
            else:
                return PinfluencerResponse.as_400_error('Invalid key in event pathParameters.product_id')
        else:
            return PinfluencerResponse(401, filter_response.get_message())