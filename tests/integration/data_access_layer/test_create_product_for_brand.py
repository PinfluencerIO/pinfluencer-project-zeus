from src.data_access_layer.image_repository import ImageException
from src.data_access_layer.product import Product
from src.data_access_layer.write_data_access import db_write_new_product_for_auth_user, NoBrandForAuthenticatedUser
from tests import InMemorySqliteDataManager, MockImageRepo, brand_generator


def test_db_write_new_product_for_auth_user_successfully():
    test_image = "test.png"
    [data_manager, image_repo, auth_user_id, brand, bytes_, payload] = common_setup({"upload": test_image})
    product = db_write_new_product_for_auth_user(data_manager=data_manager,
                                                 image_repository=image_repo,
                                                 auth_user_id=auth_user_id,
                                                 payload=payload)
    assert data_manager.changes_were_committed_once()
    assert product.name == payload['name']
    assert product.description == payload['description']
    assert product.requirements == payload['requirements']
    assert product.image == test_image
    assert image_repo.upload_was_called_once_with(
        [f'{brand.id}/{data_manager.session.query(Product).first().id}', bytes_])


def test_db_write_new_product_when_brand_does_not_exist():
    data_manager = InMemorySqliteDataManager()
    image_repo = MockImageRepo()
    try:
        db_write_new_product_for_auth_user(data_manager=data_manager,
                                           image_repository=image_repo,
                                           auth_user_id="testauthid",
                                           payload={})
        assert False
    except NoBrandForAuthenticatedUser:
        pass
    assert data_manager.changes_were_rolled_back_once()
    assert image_repo.upload_was_not_called()


def test_db_write_new_product_for_auth_user_when_image_error_occurs():
    [data_manager, image_repo, auth_user_id, brand, bytes_, payload] = common_setup({"upload": ImageException()})
    try:
        db_write_new_product_for_auth_user(data_manager=data_manager,
                                           image_repository=image_repo,
                                           auth_user_id=auth_user_id,
                                           payload=payload)
        assert False
    except ImageException:
        pass
    assert data_manager.changes_were_rolled_back_once()
    assert image_repo.upload_was_called_once_with(
        [f'{brand.id}/{data_manager.session.query(Product).first().id}', bytes_])


def common_setup(image_repo_setup):
    data_manager = InMemorySqliteDataManager()
    image_repo = MockImageRepo(image_repo_setup)
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
    return [data_manager, image_repo, auth_user_id, brand, bytes_, payload]
