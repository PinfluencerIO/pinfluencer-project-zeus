from src.data_access_layer import to_list
from src.pinfluencer_response import PinfluencerResponse
from src.processors import get_cognito_user


class ProcessGetForAuthenticatedUser:
    def __init__(self, load_for_authenticated_user, data_manager) -> None:
        self.load_for_authenticated_user = load_for_authenticated_user
        self.data_manager = data_manager

    def do_process(self, event):
        auth_user_id = get_cognito_user(event)
        loaded = self.load_for_authenticated_user(auth_user_id, self.data_manager)
        if loaded:
            return self.build_body(loaded)
        else:
            return PinfluencerResponse(404, 'Not found')

    def build_body(self, loaded):
        print(f'build body for single loaded item')
        return PinfluencerResponse(200, loaded.as_dict())


class ProcessGetForAuthenticatedUserAsCollection(ProcessGetForAuthenticatedUser):
    def build_body(self, loaded):
        print(f'build body for collection of loaded items')
        return PinfluencerResponse(200, to_list(loaded))
