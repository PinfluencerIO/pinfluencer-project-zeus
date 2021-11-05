import abc

from src.web.http_util import PinfluencerResponse

# Todo: Not sure this is the right place for an interface...read up about it.


class ProcessInterface(abc.ABC):
    @abc.abstractmethod
    def do_process(self, event: dict) -> PinfluencerResponse:
        pass
