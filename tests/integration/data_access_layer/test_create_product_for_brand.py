from src.data_access_layer.product import Product
from src.data_access_layer.write_data_access import db_write_new_product_for_auth_user
from tests import InMemorySqliteDataManager, MockImageRepo, brand_generator


def test_db_write_new_product_for_auth_user_successfully():
    data_manager = InMemorySqliteDataManager()
    test_image = "test.png"
    image_repo = MockImageRepo({"upload": test_image})
    auth_user_id = "testauthid"
    brand = brand_generator(1, auth_user_id=auth_user_id)
    data_manager.create_fake_data([brand])
    bytes_ = "testbytes"
    payload = {
        "name": "testname",
        "description": "testdesc",
        "requirements": "testrequirements",
        "image_bytes": bytes_
    }
    product = db_write_new_product_for_auth_user(data_manager=data_manager,
                                                 image_repository=image_repo,
                                                 auth_user_id=auth_user_id,
                                                 payload=payload)
    assert data_manager.commit_was_called_once()
    assert product.name == payload['name']
    assert product.description == payload['description']
    assert product.requirements == payload['requirements']
    assert product.image == test_image
    assert image_repo.upload_was_called_once_with(
        [f'{brand.id}/{data_manager.session.query(Product).first().id}', bytes_])
