from src.filters.authorised_filter import GetBrandAssociatedWithCognitoUser
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessAuthenticatedGetBrand:
    def __init__(self, auth_filter: GetBrandAssociatedWithCognitoUser, data_manager: DataManagerInterface):
        self.auth_filter = auth_filter
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_authenticated_brand(event)

        if filter_response.is_success():
            return PinfluencerResponse(filter_response.get_code(), filter_response.get_payload())
        else:
            return PinfluencerResponse(404, "No brand associated with auth_key")

    def get_authenticated_brand(self, event):
        return self.auth_filter.do_filter(event)