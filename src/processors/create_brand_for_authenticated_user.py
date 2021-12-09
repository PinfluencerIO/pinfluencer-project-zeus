from src.data_access_layer.brand import Brand
from src.data_access_layer.write_data_access import write_new_brand
from src.filters.authorised_filter import NoBrandAssociatedWithCognitoUser
from src.filters.payload_validation import BrandPostPayloadValidation
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse
from src.processors import get_user, protect_email_from_update_if_held_in_claims


class ProcessAuthenticatedPostBrand:
    def __init__(self, no_associated_brand_with_cognito_user: NoBrandAssociatedWithCognitoUser,
                 post_validation: BrandPostPayloadValidation,
                 data_manager: DataManagerInterface):
        self.post_validation = post_validation
        self.no_associated_brand_with_cognito_user = no_associated_brand_with_cognito_user
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.check_no_brand_associated_with_authenticated_user(event)
        if filter_response.is_success():
            filter_response = self.validate_new_brand_payload(event)
            if filter_response.is_success():
                payload = filter_response.get_payload()
                payload["auth_user_id"] = get_user(event=event)
                protect_email_from_update_if_held_in_claims(payload, event)
                image_bytes = payload['image']
                payload['image'] = None
                brand = self.create_new_brand(payload, image_bytes)
                return PinfluencerResponse(201, brand.as_dict())
            else:
                return PinfluencerResponse(filter_response.get_code())
        else:
            return PinfluencerResponse(filter_response.get_code())

    def create_new_brand(self, payload, image_bytes) -> Brand:
        return write_new_brand(payload, image_bytes, self.data_manager)

    def validate_new_brand_payload(self, event):
        return self.post_validation.do_filter(event)

    def check_no_brand_associated_with_authenticated_user(self, event):
        return self.no_associated_brand_with_cognito_user.do_filter(event)