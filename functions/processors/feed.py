from functions.processors import ProcessInterface
from functions.processors.hacks import old_manual_functions
from functions.web.http_util import PinfluencerResponse


class ProcessPublicFeed(ProcessInterface):
    def __init__(self):
        pass

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        return old_manual_functions.get_feed()
