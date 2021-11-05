from src.web.processors import ProcessInterface
from src.web.http_util import PinfluencerResponse
from src.data_access_layer.repositories.alchemy_product_repository import AlchemyProductRepository


class ProcessPublicFeed(ProcessInterface):
    def __init__(self):
        pass

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        return PinfluencerResponse.as_500_error("not implemented")
