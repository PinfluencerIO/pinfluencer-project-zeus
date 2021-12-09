from src.data_access_layer import to_list
from src.data_access_layer.brand import Brand
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessPublicBrands:
    def __init__(self, load_brands, data_manager: DataManagerInterface):
        self.load_brands = load_brands
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        return PinfluencerResponse(body=to_list(self.load_brands(self.data_manager)))
