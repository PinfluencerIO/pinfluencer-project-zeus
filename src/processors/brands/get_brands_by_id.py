from src.data_access_layer.brand import Brand
from src.pinfluencer_response import PinfluencerResponse
from src.processors import valid_path_resource_id


class ProcessPublicGetBrandBy:
    def __init__(self, load_by_id, data_manager):
        self.load_by_id = load_by_id
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        id_ = valid_path_resource_id(event, 'brand_id')
        if id_:
            brand = self.load_by_id(id_, Brand, self.data_manager)
            if brand:
                return PinfluencerResponse(200, brand.as_dict())
            else:
                return PinfluencerResponse(404, 'Not found')
        else:
            return PinfluencerResponse.as_400_error('Invalid path parameter id')