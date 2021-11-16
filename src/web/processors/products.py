import json

from src.data_access_layer import to_list
from src.data_access_layer.product import Product, product_from_dict
from src.interfaces.data_manager_interface import DataManagerInterface
from src.interfaces.image_repository_interface import ImageRepositoryInterface
from src.web.filters import FilterChain
from src.web.http_util import PinfluencerResponse
from src.web.processors import ProcessInterface
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
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return PinfluencerResponse(body=event['product'])


class ProcessAuthenticatedGetProductById(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
        return PinfluencerResponse(body=event["product"])


class ProcessAuthenticatedGetProduct(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filter.do_chain(event)
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
        super().__init__(data_manager)
        self.__status_manager = status_manager
        self.filter = filter_chain
        self.__image_repository = image_repository

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_chain(event)
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
        self.__status_manager.status = True
        return PinfluencerResponse(body=product.as_dict())


class ProcessAuthenticatedPutProduct(ProcessInterface):
    def __init__(self,
                 filter_chain: FilterChain,
                 data_manager: DataManagerInterface,
                 status_manager: RequestStatusManager):
        super().__init__(data_manager)
        self.__status_manager = status_manager
        self.filter = filter_chain

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_chain(event)
        product_from_req = json.loads(event['body'])
        product: Product = (self._data_manager.session
                            .query(Product)
                            .filter(Product.id == event['product']['id'])
                            .first())
        product.name = product_from_req['name']
        product.description = product_from_req['description']
        product.requirements = product_from_req['requirements']
        self._data_manager.session.flush()
        self.__status_manager.status = True
        return PinfluencerResponse(body=product)


class ProcessAuthenticatedDeleteProduct(ProcessInterface):
    def __init__(self,
                 filter_chain: FilterChain,
                 data_manager: DataManagerInterface,
                 image_repository: ImageRepositoryInterface,
                 status_manager: RequestStatusManager):
        super().__init__(data_manager)
        self.__status_manager = status_manager
        self.filter = filter_chain
        self.__image_repository = image_repository

    def do_process(self, event: dict) -> PinfluencerResponse:
        print(self)
        self.filter.do_chain(event)
        product: Product = (self._data_manager.session
                            .query(Product)
                            .filter(Product.id == event['product']['id'])
                            .first())
        self.__image_repository.delete(path=f'{product.owner.id}/{product.id}/{product.image}')
        self._data_manager.session.delete(product)
        self._data_manager.session.flush()
        self.__status_manager.status = True
        return PinfluencerResponse(body=product.as_dict())


class ProcessAuthenticatedPatchProductImage(ProcessInterface):
    def __init__(self,
                 filter_chain: FilterChain,
                 image_repository: ImageRepositoryInterface,
                 data_manager: DataManagerInterface,
                 status_manager: RequestStatusManager) -> None:
        super().__init__(data_manager)
        self.__status_manager = status_manager
        self.filters = filter_chain
        self.__image_repository = image_repository

    def do_process(self, event: dict) -> PinfluencerResponse:
        self.filters.do_chain(event)
        product: Product = self._data_manager.session.query(Product) \
            .filter(Product.id == event['product']['id']) \
            .first()
        self.__image_repository.delete(path=f'{product.owner.id}/{product.id}/{product.image}')
        product.image = self.__image_repository.upload(path=f'{product.owner.id}/{product.id}',
                                                       image_base64_encoded=json.loads(event['body'])['image'])
        self._data_manager.session.flush()
        self.__status_manager.status = True
        return PinfluencerResponse(body=product.as_dict())
