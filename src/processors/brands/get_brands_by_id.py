from src.pinfluencer_response import PinfluencerResponse


class ProcessPublicGetBrandBy:
    def __init__(self, load_resource_by_id):
        self.load_resource_by_id = load_resource_by_id

    def do_process(self, event: dict) -> PinfluencerResponse:
        response = self.load_resource_by_id.do_filter(event)
        if response.is_success():
            return PinfluencerResponse(body=response.get_payload())
        else:
            return PinfluencerResponse.as_400_error(response.get_message())
