from src.processors import ProcessInterface
from src.processors.hacks import old_manual_functions
from src.common.web.http_util import PinfluencerResponse


class ProcessPublicFeed(ProcessInterface):
    def __init__(self):
        pass

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        return old_manual_functions.get_feed()
