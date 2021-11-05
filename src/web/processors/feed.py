from src.domain.models import ModelExtensions
from src.domain.services import Container
from src.web.processors import ProcessInterface
from src.web.http_util import PinfluencerResponse


class ProcessPublicFeed(ProcessInterface):
    def __init__(self):
        pass

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        container = Container()
        return PinfluencerResponse(body=ModelExtensions.list_to_dict(container.product_repo.feed()))
