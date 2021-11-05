from src.data_access_layer.repositories.alchemy_product_repository import AlchemyProductRepository
from src.domain.models.model_extensions import ModelExtensions
from src.interfaces.contract.product_repository_interface import ProductRepositoryInterface
from src.web.processors import ProcessInterface
from src.web.processors.hacks import old_manual_functions
from src.web.http_util import PinfluencerResponse


class ProcessPublicFeed(ProcessInterface):

    __product_repo: ProductRepositoryInterface

    def __init__(self, product_repo: ProductRepositoryInterface):
        self.__product_repo = product_repo

    def do_process(self, event: dict) -> PinfluencerResponse:
        return PinfluencerResponse(body=ModelExtensions.list_to_dict(self.__product_repo.feed()))
