import json

from src.data_access_layer import to_list
from src.data_access_layer.product import Product
from src.data_access_layer.read_data_access import load_all_products
from src.filters import FilterInterface
from src.filters.valid_id_filters import LoadResourceById, valid_uuid
from src.interfaces.data_manager_interface import DataManagerInterface
from src.pinfluencer_response import PinfluencerResponse
from src.processors import ProcessInterface


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
    def __init__(self, get_brand_associated_with_cognito_user: FilterInterface, load_product_by_id_owned_by_brand,
                 data_manager: DataManagerInterface):
        super().__init__(data_manager)
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.load_product_by_id_owned_by_brand = load_product_by_id_owned_by_brand

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)
        if filter_response.is_success():
            product_id = event['pathParameters']['product_id']
            if valid_uuid(product_id):
                product = self.load_product_by_id_owned_by_brand(product_id, filter_response.get_payload(),
                                                                 self._data_manager)
                if product:
                    return PinfluencerResponse(200, product.as_dict())
                else:
                    return PinfluencerResponse(404, 'Not found')
            else:
                return PinfluencerResponse.as_400_error('Invalid key in event pathParameters.product_id')
        else:
            return PinfluencerResponse(401, filter_response.get_message())


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


class ProcessAuthenticatedPostProduct:
    def __init__(self, get_brand_associated_with_cognito_user: FilterInterface,
                 validation: FilterInterface,
                 write_new_product,
                 data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.validation = validation
        self.write_new_product = write_new_product
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)

        if filter_response.is_success():
            brand = filter_response.get_payload()
            filter_response = self.validation.do_filter(event)
            if filter_response.is_success():
                product = self.write_new_product(filter_response.get_payload(), brand['id'], self.data_manager)
                return PinfluencerResponse(201, product.as_dict())
            else:
                return PinfluencerResponse.as_400_error(filter_response.get_message())
        else:
            return PinfluencerResponse(401, filter_response.get_message())


class ProcessAuthenticatedPutProduct:
    def __init__(self, get_brand_associated_with_cognito_user: FilterInterface,
                 validation: FilterInterface,
                 update_product,
                 data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.validation = validation
        self.update_product = update_product
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)
        if filter_response.is_success():
            product_id = event['pathParameters']['product_id']

            if valid_uuid(product_id):
                filter_response = self.validation.do_filter(event)
                if filter_response.is_success():
                    product = self.update_product(filter_response.get_payload()['id'],
                                                  product_id,
                                                  json.loads(event['body']),
                                                  self.data_manager)
                    print(f'updated product {product}')
                    if product:
                        return PinfluencerResponse(200, body=product.as_dict())
                    else:
                        return PinfluencerResponse.as_400_error()
                else:
                    return PinfluencerResponse.as_400_error()
            else:
                return PinfluencerResponse.as_400_error(filter_response.get_message())
        else:
            return PinfluencerResponse(401, filter_response.get_message())


class ProcessAuthenticatedPatchProductImage:
    def __init__(self, get_brand_associated_with_cognito_user: FilterInterface,
                 validation: FilterInterface,
                 patch_product_image,
                 data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.validation = validation
        self.patch_product_image = patch_product_image
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)
        if filter_response.is_success():
            product_id = event['pathParameters']['product_id']
            brand_id = filter_response.get_payload()['id']

            if valid_uuid(product_id):
                filter_response = self.validation.do_filter(event)
                if filter_response.is_success():
                    product = self.patch_product_image(brand_id,
                                                       product_id,
                                                       json.loads(event['body'])['image'],
                                                       self.data_manager)
                    print(f'updated product {product}')
                    if product:
                        return PinfluencerResponse(200, body=product.as_dict())
                    else:
                        return PinfluencerResponse.as_400_error()
                else:
                    return PinfluencerResponse.as_400_error()
            else:
                return PinfluencerResponse.as_400_error(filter_response.get_message())
        else:
            return PinfluencerResponse(401, filter_response.get_message())


class ProcessAuthenticatedDeleteProduct:
    def __init__(self, get_brand_associated_with_cognito_user: FilterInterface,
                 delete_product, data_manager: DataManagerInterface):
        self.get_brand_associated_with_cognito_user = get_brand_associated_with_cognito_user
        self.delete_product = delete_product
        self.data_manager = data_manager

    def do_process(self, event: dict) -> PinfluencerResponse:
        filter_response = self.get_brand_associated_with_cognito_user.do_filter(event)
        if filter_response.is_success():
            product_id = event['pathParameters']['product_id']
            brand_id = filter_response.get_payload()['id']
            if valid_uuid(product_id):
                product = self.delete_product(brand_id, product_id, self.data_manager)
                if product:
                    return PinfluencerResponse(200, f"Product {product} deleted")
                else:
                    return PinfluencerResponse(404, "Not found")
            else:
                return PinfluencerResponse.as_400_error(filter_response.get_message())
        else:
            return PinfluencerResponse(401, filter_response.get_message())
