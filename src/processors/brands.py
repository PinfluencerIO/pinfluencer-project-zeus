import json

from src.data_access_layer import to_list
from src.data_access_layer.brand import Brand, brand_from_dict
from src.data_access_layer.read_data_access import load_all_products_for_brand_id
from src.data_access_layer.write_data_access import write_new_brand
from src.filters import FilterChain
from src.filters.authorised_filter import AuthFilter, OneTimeCreateBrandFilter
from src.filters.payload_validation import BrandPostPayloadValidation
from src.filters.valid_id_filters import LoadResourceById
from src.interfaces.data_manager_interface import DataManagerInterface
from src.interfaces.image_repository_interface import ImageRepositoryInterface
from src.pinfluencer_response import PinfluencerResponse
from src.processors import ProcessInterface, get_user
from src.web.request_status_manager import RequestStatusManager


class ProcessPublicBrands(ProcessInterface):
    def __init__(self, data_manager: DataManagerInterface):
        super().__init__(data_manager)

    def do_process(self, event: dict) -> PinfluencerResponse:
        return PinfluencerResponse(body=to_list(self._data_manager.session
                                                .query(Brand)
                                                .all()))


class ProcessPublicGetBrandBy:
    def __init__(self, load_resource_by_id: LoadResourceById):
        self.load_resource_by_id = load_resource_by_id

    def do_process(self, event: dict) -> PinfluencerResponse:
        response = self.load_resource_by_id.load(event)
        if response.is_success():
            return PinfluencerResponse(body=response.get_payload())
        else:
            return PinfluencerResponse.as_400_error(response.get_message())


class ProcessPublicAllProductsForBrand:
    def __init__(self, load_resource_by_id: LoadResourceById, data_manager: DataManagerInterface):
        self.load_resource_by_id = load_resource_by_id
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        response = self.load_resource_by_id.load(event)
        if response.is_success():
            brand = response.get_payload()
            products_for_brand = load_all_products_for_brand_id(brand['id'], self.data_manager)
            return PinfluencerResponse(body=(to_list(products_for_brand)))
        else:
            return PinfluencerResponse.as_400_error(response.get_message())


class ProcessAuthenticatedGetBrand:
    def __init__(self, auth_filter: AuthFilter, data_manager: DataManagerInterface):
        self.auth_filter = auth_filter
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_authenticated_brand(event)

        if filter_response.is_success():
            return PinfluencerResponse(filter_response.get_code(), filter_response.get_payload())
        else:
            return PinfluencerResponse(filter_response.get_code())

    def get_authenticated_brand(self, event):
        return self.auth_filter.do_filter(event)


class ProcessAuthenticatedPutBrand(ProcessInterface):
    def __init__(self,
                 filter_chain: FilterChain,
                 data_manager: DataManagerInterface,
                 status_manager: RequestStatusManager):
        super().__init__(data_manager, filter_chain)
        self.__status_manager = status_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        brand: Brand = self._data_manager.session.query(Brand).filter(Brand.id == event['auth_brand']['id']).first()
        brand_from_body = brand_from_dict(json.loads(event['body']))
        brand.name = brand_from_body.name
        brand.description = brand_from_body.description
        brand.website = brand_from_body.website
        brand.instahandle = brand_from_body.instahandle
        self._data_manager.session.flush()
        return PinfluencerResponse(body=brand.as_dict())


class ProcessAuthenticatedPostBrand:
    def __init__(self,
                 auth_filter: AuthFilter,
                 one_time_create: OneTimeCreateBrandFilter,
                 post_validation: BrandPostPayloadValidation,
                 data_manager: DataManagerInterface):
        self.auth_filter = auth_filter
        self.post_validation = post_validation
        self.one_time_create = one_time_create
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        # must be authenticated
        filter_response = self.must_be_authenticated(event)
        if filter_response.is_success():
            # must not be brand associated with authenticated user
            filter_response = self.check_no_brand_associated_with_authenticated_user(event)
            if filter_response.is_success():
                # validate payload
                filter_response = self.validate_new_brand_payload(event)
                if filter_response.is_success():
                    payload = filter_response.get_payload()
                    payload["auth_user_id"] = get_user(event=event)
                    image_bytes = payload['image']
                    payload['image'] = None
                    brand = self.create_new_brand(payload, image_bytes)
                    return PinfluencerResponse(201, brand.as_dict())
                else:
                    return PinfluencerResponse(filter_response.get_code())
            else:
                return PinfluencerResponse(filter_response.get_code())
        else:
            return PinfluencerResponse(filter_response.get_code())

    def create_new_brand(self, payload, image_bytes) -> Brand:
        return write_new_brand(payload, image_bytes, self.data_manager)

    def validate_new_brand_payload(self, event):
        return self.post_validation.do_filter(event)

    def check_no_brand_associated_with_authenticated_user(self, event):
        return self.one_time_create.do_filter(event)

    def must_be_authenticated(self, event):
        return self.auth_filter.do_filter(event)


class ProcessAuthenticatedPatchBrandImage(ProcessInterface):
    def __init__(self,
                 filter_chain: FilterChain,
                 data_manager: DataManagerInterface,
                 image_repository: ImageRepositoryInterface,
                 status_manager: RequestStatusManager) -> None:
        super().__init__(data_manager, filter_chain)
        self.__image_repository = image_repository
        self.__status_manager = status_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        brand: Brand = self._data_manager.session.query(Brand).filter(Brand.id == event['auth_brand']['id']).first()
        image_id = self.__image_repository.upload(f'{brand.id}', json.loads(event['body'])['image'])
        self.__image_repository.delete(f'{brand.id}/{brand.image}')
        brand.image = image_id
        self._data_manager.session.flush()
        return PinfluencerResponse(body=brand.as_dict())


def update_email(body, event):
    if ('email' in event['requestContext']['authorizer']['jwt']['claims'] and
            event['requestContext']['authorizer']['jwt']['claims']['email'] is not None):
        body['email'] = event['requestContext']['authorizer']['jwt']['claims']['email']
