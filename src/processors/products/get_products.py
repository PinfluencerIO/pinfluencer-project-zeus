from src.data_access_layer import to_list
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessPublicProducts:
    def __init__(self, load_all_products, data_manager: DataManagerInterface):
        self.load_all_products = load_all_products
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        list_of_all_products = to_list(self.load_all_products(self.data_manager))
        return PinfluencerResponse(body=list_of_all_products)
