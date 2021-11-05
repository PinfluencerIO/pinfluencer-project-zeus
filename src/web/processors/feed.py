from src.interfaces.contract.product_repository_interface import ProductRepositoryInterface
from src.web.processors import ProcessInterface
from src.web.processors.hacks import old_manual_functions
from src.web.http_util import PinfluencerResponse


class ProcessPublicFeed(ProcessInterface):
    def __init__(self, product_repo: ProductRepositoryInterface):
        self.__product_repo = product_repo

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        return old_manual_functions.get_feed()