import json

from src.data_access_layer import to_list
from src.data_access_layer.product import Product, product_from_dict
from src.interfaces.data_manager_interface import DataManagerInterface
from src.interfaces.image_repository_interface import ImageRepositoryInterface
from src.filters import FilterChain
from src.pinfluencer_response import PinfluencerResponse
from src.processors import ProcessInterface
# Todo: Implement all these processors
from src.web.request_status_manager import RequestStatusManager


class ProcessPublicProducts(ProcessInterface):
    def __init__(self, data_manager: DataManagerInterface):
        super().__init__(data_manager)

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        return PinfluencerResponse(body=to_list(self._data_manager.session.query(Product).all()))


class ProcessPublicGetProductBy(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager, filter_chain)

    def do_process(self, event: dict) -> PinfluencerResponse:
        return PinfluencerResponse(body=event['product'])


class ProcessAuthenticatedGetProductById(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager, filter_chain)

    def do_process(self, event: dict) -> PinfluencerResponse:
        return PinfluencerResponse(body=event["product"])


class ProcessAuthenticatedGetProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager, filter_chain)

    def do_process(self, event: dict) -> PinfluencerResponse:
        products: list[Product] = (self._data_manager.session
                                   .query(Product)
                                   .filter(Product.brand_id == event["auth_brand"]['id'])
                                   .all())
        return PinfluencerResponse(body=to_list(products))


class ProcessAuthenticatedPostProduct(ProcessInterface):
    def __init__(self,
                 filter_chain: FilterChain,
                 data_manager: DataManagerInterface,
                 image_repository: ImageRepositoryInterface,
                 status_manager: RequestStatusManager):
        super().__init__(data_manager, filter_chain)
        self.__status_manager = status_manager
        self.__image_repository = image_repository

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        product_dict: dict = json.loads(event['body'])
        brand_id: str = event['auth_brand']['id']
        image = product_dict['image']
        product_dict['brand_id'] = brand_id
        product: Product = product_from_dict(product=product_dict)
        self._data_manager.session.add(product)
        self._data_manager.session.flush()
        product.image = self.__image_repository.upload(path=f'{brand_id}/{product.id}',
                                                       image_base64_encoded=image)
        self._data_manager.session.add(product)
        self._data_manager.session.flush()
        return PinfluencerResponse(body=product.as_dict())


class ProcessAuthenticatedPutProduct(ProcessInterface):
    def __init__(self,
                 filter_chain: FilterChain,
                 data_manager: DataManagerInterface,
                 status_manager: RequestStatusManager):
        super().__init__(data_manager, filter_chain)
        self.__status_manager = status_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        product_from_req = json.loads(event['body'])
        product: Product = (self._data_manager.session
                            .query(Product)
                            .filter(Product.id == event['product']['id'])
                            .first())
        product.name = product_from_req['name']
        product.description = product_from_req['description']
        product.requirements = product_from_req['requirements']
        self._data_manager.session.flush()
        return PinfluencerResponse(body=product.as_dict())


class ProcessAuthenticatedDeleteProduct(ProcessInterface):
    def __init__(self,
                 filter_chain: FilterChain,
                 data_manager: DataManagerInterface,
                 image_repository: ImageRepositoryInterface,
                 status_manager: RequestStatusManager):
        super().__init__(data_manager, filter_chain)
        self.__status_manager = status_manager
        self.__image_repository = image_repository

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        product: Product = (self._data_manager.session
                            .query(Product)
                            .filter(Product.id == event['product']['id'])
                            .first())
        self.__image_repository.delete(path=f'{product.owner.id}/{product.id}/{product.image}')
        self._data_manager.session.delete(product)
        self._data_manager.session.flush()
        return PinfluencerResponse(body=product.as_dict())


class ProcessAuthenticatedPatchProductImage(ProcessInterface):
    def __init__(self,
                 filter_chain: FilterChain,
                 image_repository: ImageRepositoryInterface,
                 data_manager: DataManagerInterface,
                 status_manager: RequestStatusManager) -> None:
        super().__init__(data_manager, filter_chain)
        self.__status_manager = status_manager
        self.__image_repository = image_repository

    def do_process(self, event: dict) -> PinfluencerResponse:
        product: Product = self._data_manager.session.query(Product) \
            .filter(Product.id == event['product']['id']) \
            .first()
        self.__image_repository.delete(path=f'{product.owner.id}/{product.id}/{product.image}')
        product.image = self.__image_repository.upload(path=f'{product.owner.id}/{product.id}',
                                                       image_base64_encoded=json.loads(event['body'])['image'])
        self._data_manager.session.flush()
        return PinfluencerResponse(body=product.as_dict())
