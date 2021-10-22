from functions.processors import ProcessInterface
from functions.web.http_util import PinfluencerResponse


class ProcessPublicFeed(ProcessInterface):
    def __init__(self):
        pass

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        return PinfluencerResponse(status_code=200, body={'message': 'ProcessPublicFeed'})