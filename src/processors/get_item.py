from src.data_access_layer import to_list
from src.pinfluencer_response import PinfluencerResponse
from src.processors import types


class ProcessGetItem:
    def __init__(self, type_, load_item, data_manager) -> None:
        super().__init__()
        self.type_ = type_
        self.load_item = load_item
        self.data_manager = data_manager

    def do_process(self, event):
        item = self.load_item(types[self.type_]['type'], self.data_manager)
        return PinfluencerResponse(200, item.as_dict())
