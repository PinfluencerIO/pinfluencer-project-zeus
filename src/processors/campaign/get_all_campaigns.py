from src.pinfluencer_response import PinfluencerResponse
from src.processors import get_cognito_user


class ProcessGetAllMyCampaigns:
    def __init__(self, data_manager, get_all_campaigns_for_authenticated_user) -> None:
        super().__init__()
        self._data_manager = data_manager
        self._get_all_campaigns_for_authenticated_user = get_all_campaigns_for_authenticated_user

    def do_process(self, event):
        auth_user_id = get_cognito_user(event)
        result = self._get_all_campaigns_for_authenticated_user(auth_user_id, self._data_manager)
        return PinfluencerResponse(200, result)
