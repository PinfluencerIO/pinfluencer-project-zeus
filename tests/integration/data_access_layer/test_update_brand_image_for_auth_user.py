from src.data_access_layer.brand import Brand
from src.data_access_layer.image_repository import ImageException
from src.data_access_layer.write_data_access import db_write_patch_brand_image_for_auth_user, \
    NoBrandForAuthenticatedUser
from tests import InMemorySqliteDataManager, MockImageRepo, brand_generator


def test_db_write_patch_brand_image_for_auth_user_successfully():
    data_manager = InMemorySqliteDataManager()
    auth_id = "testauthid"
    prev_image = "prev.png"
    brand = brand_generator(1, auth_id, prev_image)
    data_manager.create_fake_data([brand])
    next_image = "test.png"
    bytes_ = "testbytes"
    image_repo = MockImageRepo({"upload": next_image})
    brand_in_db = db_write_patch_brand_image_for_auth_user(auth_user_id=auth_id,
                                                           payload={"image_bytes": bytes_},
                                                           data_manager=data_manager,
                                                           image_repository=image_repo)
    assert image_repo.received('upload', 1)
    assert image_repo.received_with_args('upload', [brand.id, bytes_])
    assert image_repo.received('delete', 1)
    assert image_repo.received_with_args('delete', [f'{brand.id}/{prev_image}'])
    assert brand_in_db.image == next_image
    assert data_manager.received('commit', 1)


def test_db_write_patch_brand_image_when_brand_does_not_exist():
    data_manager = InMemorySqliteDataManager()
    image_repo = MockImageRepo()
    try:
        db_write_patch_brand_image_for_auth_user(auth_user_id="",
                                                 payload={},
                                                 data_manager=data_manager,
                                                 image_repository=image_repo)
        assert False
    except NoBrandForAuthenticatedUser:
        pass
    assert image_repo.did_not_receive('upload')
    assert image_repo.did_not_receive('delete')
    assert data_manager.did_not_receive('commit')


def test_db_write_patch_brand_image_when_upload_image_error_occurs():
    data_manager = InMemorySqliteDataManager()
    auth_id = "testauthid"
    prev_image = "prev.png"
    brand = brand_generator(1, auth_id, prev_image)
    data_manager.create_fake_data([brand])
    bytes_ = "testbytes"
    image_repo = MockImageRepo({"upload": ImageException()})
    try:
        db_write_patch_brand_image_for_auth_user(auth_user_id=auth_id,
                                                 payload={"image_bytes": bytes_},
                                                 data_manager=data_manager,
                                                 image_repository=image_repo)
        assert False
    except ImageException:
        pass
    assert image_repo.received('upload', 1)
    assert image_repo.received_with_args('upload', [brand.id, bytes_])
    assert image_repo.did_not_receive('delete')
    brand_in_db = data_manager.session.query(Brand).first()
    assert brand_in_db.image == prev_image
    assert data_manager.did_not_receive('commit')


def test_db_write_patch_brand_image_when_delete_image_error_occurs():
    data_manager = InMemorySqliteDataManager()
    auth_id = "testauthid"
    prev_image = "prev.png"
    next_image = "test.png"
    brand = brand_generator(1, auth_id, prev_image)
    data_manager.create_fake_data([brand])
    bytes_ = "testbytes"
    image_repo = MockImageRepo({
        "delete": ImageException(),
        "upload": next_image
    })
    db_write_patch_brand_image_for_auth_user(auth_user_id=auth_id,
                                             payload={"image_bytes": bytes_},
                                             data_manager=data_manager,
                                             image_repository=image_repo)
    assert image_repo.received('upload', 1)
    assert image_repo.received_with_args('upload', [brand.id, bytes_])
    assert image_repo.received('delete', 1)
    assert image_repo.received_with_args('delete', [f'{brand.id}/{prev_image}'])
    brand_in_db = data_manager.session.query(Brand).first()
    assert brand_in_db.image == next_image
    assert data_manager.received('commit', 1)
