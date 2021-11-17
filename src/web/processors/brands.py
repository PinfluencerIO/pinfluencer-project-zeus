import json

from src.data_access_layer import to_list
from src.data_access_layer.brand import Brand, brand_from_dict
from src.data_access_layer.product import Product
from src.interfaces.data_manager_interface import DataManagerInterface
from src.interfaces.image_repository_interface import ImageRepositoryInterface
from src.web.filters import FilterChain
from src.web.http_util import PinfluencerResponse
from src.web.processors import ProcessInterface, get_user
from src.web.request_status_manager import RequestStatusManager


class ProcessPublicBrands(ProcessInterface):
    def __init__(self, data_manager: DataManagerInterface):
        super().__init__(data_manager)

    def do_process(self, event: dict) -> PinfluencerResponse:
        return PinfluencerResponse(body=to_list(self._data_manager.session
                                                .query(Brand)
                                                .all()))


class ProcessPublicGetBrandBy(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager, filter_chain)

    def do_process(self, event: dict) -> PinfluencerResponse:
        return PinfluencerResponse(body=event["brand"])


class ProcessPublicAllProductsForBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager, filter_chain)

    def do_process(self, event: dict) -> PinfluencerResponse:
        return PinfluencerResponse(body=to_list(self._data_manager.session
                                                .query(Product)
                                                .filter(Product.brand_id == event['brand']['id'])
                                                .all()))


class ProcessAuthenticatedGetBrand(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager, filter_chain)

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(f'found auth brand {event["auth_brand"]}')
        return PinfluencerResponse(body=event["auth_brand"])


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


class ProcessAuthenticatedPostBrand(ProcessInterface):
    def __init__(self,
                 filter_chain: FilterChain,
                 data_manager: DataManagerInterface,
                 image_repository: ImageRepositoryInterface,
                 status_manager: RequestStatusManager):
        super().__init__(data_manager, filter_chain)
        self.__image_repository = image_repository
        self.__status_manager = status_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        brand_dict = json.loads(event['body'])
        update_email(brand_dict, event)
        brand_dict["auth_user_id"] = get_user(event=event)
        image_bytes = brand_dict['image']
        brand_dict['image'] = None
        brand = brand_from_dict(brand_dict)

        self._data_manager.session.add(brand)
        self._data_manager.session.flush()
        image_id = self.__image_repository.upload(f'{brand.id}', image_bytes)
        brand: Brand = self._data_manager.session.query(Brand) \
            .filter(Brand.id == brand.id) \
            .first()
        brand.image = image_id
        self._data_manager.session.flush()
        return PinfluencerResponse(body=brand.as_dict(), status_code=201)


def update_email(body, event):
    if ('email' in event['requestContext']['authorizer']['jwt']['claims'] and
            event['requestContext']['authorizer']['jwt']['claims']['email'] is not None):
        body['email'] = event['requestContext']['authorizer']['jwt']['claims']['email']


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
