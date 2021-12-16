from src.data_access_layer import to_list
from src.pinfluencer_response import PinfluencerResponse
from src.processors import types


class ProcessGetCollection:
    def __init__(self, type_, load_collection, data_manager) -> None:
        super().__init__()
        self.type_ = type_
        self.load_collection = load_collection
        self.data_manager = data_manager

    def do_process(self, event):
        collection = self.load_collection(types[self.type_]['type'], self.data_manager)
        print('collection')
        print(collection)
        return PinfluencerResponse(200, to_list(collection))
