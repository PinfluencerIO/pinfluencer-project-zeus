from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse
from src.processors import protect_email_from_update_if_held_in_claims


class ProcessAuthenticatedPutBrand:
    def __init__(self,
                 get_brand_associated_with_cognito_user,
                 put_validation,
                 update_brand,
                 data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.put_validation = put_validation
        self.update_brand = update_brand
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)
        if filter_response.is_success():

            brand = filter_response.get_payload().as_dict()
            filter_response = self.put_validation.do_filter(event)
            if filter_response.is_success():
                protect_email_from_update_if_held_in_claims(filter_response.get_payload(), event)
                id_ = brand['id']
                payload = filter_response.get_payload()
                updated_brand = self.update_brand(id_, payload, self.data_manager)
                return PinfluencerResponse(200, updated_brand.as_dict())
            else:
                return PinfluencerResponse(filter_response.get_code(), filter_response.get_message())
        else:
            return PinfluencerResponse(401, filter_response.get_message())
