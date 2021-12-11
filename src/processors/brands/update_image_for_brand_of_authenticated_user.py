from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessAuthenticatedPatchBrandImage:
    def __init__(self,
                 get_brand_associated_with_cognito_user,
                 brand_image_patch_payload_validation,
                 update_brand_image,
                 data_manager: DataManagerInterface) -> None:
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.brand_image_patch_payload_validation = brand_image_patch_payload_validation
        self.update_brand_image = update_brand_image
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)
        if filter_response.is_success():
            brand = filter_response.get_payload().as_dict()
            filter_response = self.brand_image_patch_payload_validation.do_filter(event)
            if filter_response.is_success():
                filter_response = self.brand_image_patch_payload_validation.do_filter(event)
                if filter_response.is_success():
                    updated_brand = self.update_brand_image(brand['id'],
                                                            filter_response.get_payload()['image'],
                                                            self.data_manager)
                    return PinfluencerResponse(200, updated_brand.as_dict())
                else:
                    return PinfluencerResponse(filter_response.get_code(), filter_response.get_message())
            else:
                return PinfluencerResponse(filter_response.get_code(), filter_response.get_message())
        else:
            return PinfluencerResponse(filter_response.get_code(), filter_response.get_message())
