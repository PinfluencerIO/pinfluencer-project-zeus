from src.data_access_layer.write_data_access import NotFoundException
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse
from src.processors import valid_uuid, get_cognito_user


class ProcessAuthenticatedDeleteProduct:
    def __init__(self, delete_product, data_manager: DataManagerInterface):
        self.delete_product = delete_product
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        product_id = event['pathParameters']['product_id']
        if valid_uuid(product_id):
            auth_user_id = get_cognito_user(event)
            try:
                product = self.delete_product(auth_user_id, product_id, self.data_manager)
            except NotFoundException as nfe:
                return PinfluencerResponse(404, str(nfe))
            return PinfluencerResponse(200, f'Delete {product}')
        else:
            return PinfluencerResponse.as_400_error('Invalid product id')
