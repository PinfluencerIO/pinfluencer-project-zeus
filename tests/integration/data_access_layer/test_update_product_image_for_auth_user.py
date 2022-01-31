from src.data_access_layer.image_repository import ImageException
from src.data_access_layer.write_data_access import db_write_patch_product_image_for_auth_user, \
    NoBrandForAuthenticatedUser, NotFoundException
from tests import InMemorySqliteDataManager, brand_generator, product_generator, MockImageRepo


def test_db_write_patch_product_image_for_auth_user_successfully():
    next_image = "test.png"
    [data_manager, image_repo, brand, product, bytes_, prev_image, auth_id] = common_setup(image_repo_setup={
        "upload": next_image
    })
    brand_in_db = db_write_patch_product_image_for_auth_user(auth_user_id=auth_id,
                                                             payload={
                                                                 "image_bytes": bytes_,
                                                                 "product_id": product.id
                                                             },
                                                             data_manager=data_manager,
                                                             image_repository=image_repo)
    assert image_repo.upload_was_called_once_with([f'{brand.id}/{product.id}', bytes_])
    assert image_repo.delete_was_called_once_with([f'{brand.id}/{product.id}/{prev_image}'])
    assert brand_in_db.image == next_image
    assert data_manager.changes_were_committed_once()


def test_db_write_patch_product_image_when_brand_does_not_exist():
    data_manager = InMemorySqliteDataManager()
    image_repo = MockImageRepo()
    try:
        db_write_patch_product_image_for_auth_user(auth_user_id="",
                                                   payload={},
                                                   data_manager=data_manager,
                                                   image_repository=image_repo)
        assert False
    except NoBrandForAuthenticatedUser:
        pass
    assert image_repo.upload_was_not_called()
    assert image_repo.delete_was_not_called()
    assert data_manager.no_changes_were_rolled_back_or_committed()


def test_db_write_patch_product_image_when_product_does_not_exist():
    data_manager = InMemorySqliteDataManager()
    auth_id = "testauthid"
    data_manager.create_fake_data([brand_generator(1, auth_id)])
    image_repo = MockImageRepo()
    try:
        db_write_patch_product_image_for_auth_user(auth_user_id=auth_id,
                                                   payload={"product_id": "testid"},
                                                   data_manager=data_manager,
                                                   image_repository=image_repo)
        assert False
    except NotFoundException:
        pass
    assert image_repo.upload_was_not_called()
    assert image_repo.delete_was_not_called()
    assert data_manager.no_changes_were_rolled_back_or_committed()


def test_db_write_patch_product_image_for_auth_user_when_upload_image_error_occurs():
    [data_manager, image_repo, brand, product, bytes_, _, auth_id] = common_setup(image_repo_setup={
        "upload": ImageException()
    })
    try:
        db_write_patch_product_image_for_auth_user(auth_user_id=auth_id,
                                                   payload={
                                                       "image_bytes": bytes_,
                                                       "product_id": product.id
                                                   },
                                                   data_manager=data_manager,
                                                   image_repository=image_repo)
        assert False
    except ImageException:
        pass
    assert image_repo.upload_was_called_once_with([f'{brand.id}/{product.id}', bytes_])
    assert image_repo.delete_was_not_called()
    assert data_manager.changes_were_rolled_back_once()


def test_db_write_patch_product_image_for_auth_user_when_delete_image_error_occurs():
    next_image = "test.png"
    [data_manager, image_repo, brand, product, bytes_, prev_image, auth_id] = common_setup(image_repo_setup={
        "upload": next_image,
        "delete": ImageException()
    })
    brand_in_db = db_write_patch_product_image_for_auth_user(auth_user_id=auth_id,
                                                             payload={
                                                                 "image_bytes": bytes_,
                                                                 "product_id": product.id
                                                             },
                                                             data_manager=data_manager,
                                                             image_repository=image_repo)
    assert image_repo.upload_was_called_once_with([f'{brand.id}/{product.id}', bytes_])
    assert image_repo.delete_was_called_once_with([f'{brand.id}/{product.id}/{prev_image}'])
    assert brand_in_db.image == next_image
    assert data_manager.changes_were_committed_once()


def common_setup(image_repo_setup):
    data_manager = InMemorySqliteDataManager()
    auth_id = "testauthid"
    prev_image = "prev.png"
    brand = brand_generator(1, auth_id)
    product = product_generator(1, brand=brand, image=prev_image)
    bytes_ = "testbytes"
    data_manager.create_fake_data([brand, product])
    image_repo = MockImageRepo(image_repo_setup)
    return [data_manager, image_repo, brand, product, bytes_, prev_image, auth_id]