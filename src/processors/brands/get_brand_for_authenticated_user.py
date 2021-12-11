from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessGetAuthenticatedBrand:
    def __init__(self, get_brand_associated_with_cognito_user, data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)

        if filter_response.is_success():
            return PinfluencerResponse(filter_response.get_code(), filter_response.get_payload().as_dict())
        else:
            return PinfluencerResponse(404, "No brand associated with auth_key")
