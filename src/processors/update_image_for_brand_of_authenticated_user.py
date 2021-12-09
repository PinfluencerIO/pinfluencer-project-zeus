from src.filters import FilterInterface
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse


class ProcessAuthenticatedPatchBrandImage:
    def __init__(self,
                 auth_filter: FilterInterface,
                 brand_image_patch_payload_validation: FilterInterface,
                 update_brand_image,
                 data_manager: DataManagerInterface) -> None:
        self.auth_filter = auth_filter
        self.brand_image_patch_payload_validation = brand_image_patch_payload_validation
        self.update_brand_image = update_brand_image
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.auth_filter.do_filter(event)
        if filter_response.is_success():
            brand = filter_response.get_payload()
            filter_response = self.brand_image_patch_payload_validation.do_filter(event)
            if filter_response.is_success():
                filter_response = self.brand_image_patch_payload_validation.do_filter(event)
                if filter_response.is_success():
                    updated_brand = self.update_brand_image(brand['id'],
                                                            filter_response.get_payload()['image'],
                                                            self.data_manager)
                    return PinfluencerResponse(200, updated_brand.as_dict())
                else:
                    return PinfluencerResponse(filter_response.get_code(), filter_response.get_message())
            else:
                return PinfluencerResponse(filter_response.get_code(), filter_response.get_message())
        else:
            return PinfluencerResponse(filter_response.get_code(), filter_response.get_message())