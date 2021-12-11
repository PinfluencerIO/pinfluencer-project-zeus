import uuid

from src.data_access_layer.brand import Brand
from src.data_access_layer.product import Product
from src.filters import FilterResponse


def mock_load_brands(data_manager):
    brand1 = Brand()
    brand1.id = str(uuid.UUID)
    brand2 = Brand()
    brand2.id = str(uuid.UUID)
    return [brand1, brand2]


def mock_load_all_products_for_brand_id(brand_id, data_manager):
    brand = Brand()
    brand.id = brand_id
    product1_1 = Product()
    product1_1.brand = brand
    product2_1 = Product()
    product2_1.brand = brand
    product3_1 = Product()
    product3_1.brand = brand

    return [product1_1, product2_1, product3_1]


class MockFilterResponse:
    def __init__(self, response) -> None:
        self.response = response

    def do_filter(self, event: dict) -> FilterResponse:
        return self.response


def mock_successful_db_call(id_, payload, data_manager):
    return Brand()


def mock_db_call_with_exception(_id, payload, data_manager):
    raise Exception('db issue')


user_id = 'user_id'
email = 'do@notupdate.email'
event_cognito_user = {
    'requestContext': {
        'authorizer': {
            'jwt': {
                'claims': {
                    'cognito:username': user_id,
                    'email': email
                }
            }
        }
    },
    'body': {
        'image': 'image bytes',
        'email': 'new@email.should.not.update.com'
    }
}


def mock_successful_update_brand_image(brand_id, image_bytes, data_manager):
    return Brand()


def mock_update_brand_image_raise_exception(brand_id, image_bytes, data_manager):
    raise Exception('Db issue')
