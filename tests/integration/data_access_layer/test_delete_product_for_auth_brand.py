from src.data_access_layer.product import Product
from src.data_access_layer.repositories import ImageException
from src.data_access_layer.write_data_access import delete_product, NotFoundException, NoBrandForAuthenticatedUser
from tests import InMemorySqliteDataManager, brand_generator, MockImageRepo, product_generator


def test_db_delete_new_product_for_auth_user_successfully():
    test_image = "test.png"
    [data_manager, image_repo, auth_user_id, brand, product] = common_setup({"upload": test_image})
    delete_product(data_manager=data_manager,
                   image_repository=image_repo,
                   auth_user_id=auth_user_id,
                   product_id=product.id)
    deleted_product = data_manager.get_last_uncommitted_or_committed_deleted_entity()
    assert data_manager.changes_were_committed_once()
    assert data_manager.session.query(Product).first() is None
    assert image_repo.delete_was_called_once_with(
        [f'{brand.id}/{deleted_product.id}/{deleted_product.image}'])


def test_db_delete_new_product_when_brand_does_not_exist():
    data_manager = InMemorySqliteDataManager()
    image_repo = MockImageRepo()
    try:
        delete_product(data_manager=data_manager,
                       image_repository=image_repo,
                       auth_user_id="testid1",
                       product_id="testid2")
        assert False
    except NoBrandForAuthenticatedUser:
        pass
    assert data_manager.no_changes_were_rolled_back_or_committed()
    assert image_repo.upload_was_not_called()


def test_db_delete_new_product_for_auth_user_when_image_error_occurs():
    [data_manager, image_repo, auth_user_id, brand, product] = common_setup({"delete": ImageException()})
    delete_product(data_manager=data_manager,
                   image_repository=image_repo,
                   auth_user_id=auth_user_id,
                   product_id=product.id)
    assert data_manager.changes_were_committed_once()
    assert image_repo.delete_was_called_once_with(
        [f'{brand.id}/{product.id}/{product.image}'])


def test_db_delete_product_for_auth_user_when_product_doesnt_exist():
    data_manager = InMemorySqliteDataManager()
    auth_user_id = "testid"
    data_manager.create_fake_data([brand_generator(1, auth_user_id=auth_user_id)])
    image_repository = MockImageRepo()
    try:
        delete_product(auth_user_id=auth_user_id,
                       data_manager=data_manager,
                       image_repository=image_repository,
                       product_id="testid")
        assert False
    except NotFoundException:
        pass
    assert data_manager.no_changes_were_rolled_back_or_committed()


def common_setup(image_repo_setup):
    data_manager = InMemorySqliteDataManager()
    image_repo = MockImageRepo(image_repo_setup)
    auth_user_id = "testauthid"
    brand = brand_generator(1, auth_user_id=auth_user_id)
    product = product_generator(1, brand=brand)
    data_manager.create_fake_data([brand, product])
    return [data_manager, image_repo, auth_user_id, brand, product]
