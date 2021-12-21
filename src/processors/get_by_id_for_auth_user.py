from src.pinfluencer_response import PinfluencerResponse
from src.processors import valid_path_resource_id, types, get_cognito_user


class ProcessGetByForAuthenticatedUser:
    def __init__(self, load_by_id_for_auth_id, type_, data_manager):
        self.type_ = type_
        self.load_by_id_for_auth_id = load_by_id_for_auth_id
        self.data_manager = data_manager

    def do_process(self, event) -> PinfluencerResponse:
        resource_id = valid_path_resource_id(event, types[self.type_]['key'])
        if resource_id:
            auth_user_id = get_cognito_user(event)
            resource = self.load_by_id_for_auth_id(resource_id, auth_user_id, self.data_manager)
            if resource:
                return PinfluencerResponse(200, resource.as_dict())
            else:
                return PinfluencerResponse(404, 'Not found')
        else:
            return PinfluencerResponse.as_400_error(f'{self} Invalid path parameter id')
