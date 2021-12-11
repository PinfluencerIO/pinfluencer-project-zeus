from src.filters.valid_id_filters import valid_uuid
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessAuthenticatedPatchProductImage:
    def __init__(self, get_brand_associated_with_cognito_user,
                 validation,
                 patch_product_image,
                 data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.validation = validation
        self.patch_product_image = patch_product_image
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)
        if filter_response.is_success():
            product_id = event['pathParameters']['product_id']
            brand_id = filter_response.get_payload().as_dict()['id']

            if valid_uuid(product_id):
                filter_response = self.validation.do_filter(event)
                if filter_response.is_success():
                    body = filter_response.get_payload()

                    product = self.patch_product_image(brand_id,
                                                       product_id,
                                                       body['image'],
                                                       self.data_manager)
                    print(f'updated product {product}')
                    if product:
                        return PinfluencerResponse(200, body=product.as_dict())
                    else:
                        return PinfluencerResponse.as_400_error()
                else:
                    return PinfluencerResponse.as_400_error()
            else:
                return PinfluencerResponse.as_400_error(filter_response.get_message())
        else:
            return PinfluencerResponse(401, filter_response.get_message())