import json

from src.data_access_layer import to_list
from src.data_access_layer.product import Product, product_from_dict
from src.data_access_layer.read_data_access import load_all_products
from src.filters.valid_id_filters import LoadResourceById
from src.interfaces.data_manager_interface import DataManagerInterface
from src.interfaces.image_repository_interface import ImageRepositoryInterface
from src.filters import FilterChain, FilterInterface
from src.pinfluencer_response import PinfluencerResponse
from src.processors import ProcessInterface
# Todo: Implement all these processors
from src.web.request_status_manager import RequestStatusManager


class ProcessPublicProducts:
    def __init__(self, data_manager: DataManagerInterface):
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        list_of_all_products = to_list(self.load_all_products())
        return PinfluencerResponse(body=list_of_all_products)

    def load_all_products(self):
        return load_all_products(self.data_manager)


class ProcessPublicGetProductBy:
    def __init__(self, load_resource_by_id: LoadResourceById, data_manager: DataManagerInterface):
        self.load_resource_by_id = load_resource_by_id
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        response = self.load_product_from_cmd(event)
        if response.is_success():
            return PinfluencerResponse(body=response.get_payload())
        else:
            return PinfluencerResponse.as_400_error(response.get_message())

    def load_product_from_cmd(self, event):
        return self.load_resource_by_id.load(event)


class ProcessAuthenticatedGetProductById(ProcessInterface):
    def __init__(self, filter_chain: FilterChain, data_manager: DataManagerInterface):
        super().__init__(data_manager, filter_chain)

    def do_process(self, event: dict) -> PinfluencerResponse:
        return PinfluencerResponse(body=event["product"])


class ProcessAuthenticatedGetProducts:
    def __init__(self, get_brand_associated_with_cognito_user: FilterInterface,
                 load_all_products_for_brand_id,
                 data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.load_all_products_for_brand_id = load_all_products_for_brand_id
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)

        if filter_response.is_success():
            products: list[Product] = self.load_all_products_for_brand_id(
                filter_response.get_payload()['id'],
                self.data_manager)
            return PinfluencerResponse(body=to_list(products))
        else:
            return PinfluencerResponse(401, filter_response.get_message())


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
