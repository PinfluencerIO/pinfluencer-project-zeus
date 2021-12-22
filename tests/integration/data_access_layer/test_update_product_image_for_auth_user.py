from src.data_access_layer.write_data_access import db_write_patch_product_image_for_auth_user
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


def common_setup(image_repo_setup):
    data_manager = InMemorySqliteDataManager()
    auth_id = "testauthid"
    prev_image = "prev.png"
    brand = brand_generator(1, auth_id, prev_image)
    product = product_generator(1, brand=brand)
    bytes_ = "testbytes"
    data_manager.create_fake_data([brand, product])
    image_repo = MockImageRepo(image_repo_setup)
    return [data_manager, image_repo, brand, product, bytes_, prev_image, auth_id]
