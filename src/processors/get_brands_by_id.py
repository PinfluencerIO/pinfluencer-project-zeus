from src.filters.valid_id_filters import LoadResourceById
from src.pinfluencer_response import PinfluencerResponse


class ProcessPublicGetBrandBy:
    def __init__(self, load_resource_by_id: LoadResourceById):
        self.load_resource_by_id = load_resource_by_id

    def do_process(self, event: dict) -> PinfluencerResponse:
        response = self.load_resource_by_id.load(event)
        if response.is_success():
            return PinfluencerResponse(body=response.get_payload())
        else:
            return PinfluencerResponse.as_400_error(response.get_message())