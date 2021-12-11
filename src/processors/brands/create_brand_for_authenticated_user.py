from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse
from src.processors import get_user, protect_email_from_update_if_held_in_claims


class ProcessAuthenticatedPostBrand:
    def __init__(self, no_associated_brand_with_cognito_user,
                 post_validation,
                 create_new_brand,
                 data_manager: DataManagerInterface):
        self.no_associated_brand_with_cognito_user = no_associated_brand_with_cognito_user
        self.post_validation = post_validation
        self.create_new_brand = create_new_brand
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.no_associated_brand_with_cognito_user.do_filter(event)
        if filter_response.is_success():
            filter_response = self.post_validation.do_filter(event)
            if filter_response.is_success():
                payload = filter_response.get_payload()
                payload["auth_user_id"] = get_user(event=event)
                protect_email_from_update_if_held_in_claims(payload, event)
                image_bytes = payload['image']
                payload['image'] = None
                brand = self.create_new_brand(payload, image_bytes, self.data_manager)
                return PinfluencerResponse(201, brand.as_dict())
            else:
                return PinfluencerResponse(filter_response.get_code())
        else:
            return PinfluencerResponse(filter_response.get_code(), 'Brand already associated with auth id')
