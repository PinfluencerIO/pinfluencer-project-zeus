import abc

from src.common.web.http_util import PinfluencerResponse

# Todo: Not sure this is the right place for an interface...read up about it.


class ProcessInterface:
    @abc.abstractmethod
    def do_process(self, event: dict) -> PinfluencerResponse:
        pass
