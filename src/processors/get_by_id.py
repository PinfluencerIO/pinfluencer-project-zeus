from src.pinfluencer_response import PinfluencerResponse
from src.processors import valid_path_resource_id, types


class ProcessGetBy:
    def __init__(self, load_by_id, type_, data_manager):
        self.load_by_id = load_by_id
        self.type_ = type_
        self.data_manager = data_manager

    def do_process(self, event) -> PinfluencerResponse:
        id_ = valid_path_resource_id(event, types[self.type_]['key'])
        if id_:
            resource = self.load_by_id(id_, types[self.type_]['type'], self.data_manager)
            if resource:
                return PinfluencerResponse(200, resource.as_dict())
            else:
                return PinfluencerResponse(404, 'Not found')
        else:
            return PinfluencerResponse.as_400_error(f'{self} Invalid path parameter id')
