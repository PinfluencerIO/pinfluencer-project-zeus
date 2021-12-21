from src.data_access_layer.image_repository import ImageException
from src.data_access_layer.write_data_access import db_write_new_brand_for_auth_user, AlreadyExistsException
from tests import InMemorySqliteDataManager, MockImageRepo, brand_generator


def test_db_write_new_brand_for_auth_user_when_record_is_written_successfully():
    test_image = "test.png"
    image_repo = MockImageRepo({"upload": test_image})
    bytes_ = "test bytes"
    [data_manager, payload] = setup_data(bytes_)
    test_auth_id = "test auth id"
    brand_in_db = db_write_new_brand_for_auth_user(auth_user_id=test_auth_id,
                                                   payload=payload,
                                                   data_manager=data_manager,
                                                   image_repository=image_repo)
    assert image_repo.received('upload', 1) and image_repo.received_with_args('upload', [f'{brand_in_db.id}', bytes_])
    assert brand_in_db.name == payload['name']
    assert brand_in_db.description == payload['description']
    assert brand_in_db.website == payload['website']
    assert brand_in_db.email == payload['email']
    assert brand_in_db.instahandle == payload['instahandle']
    assert brand_in_db.image == test_image
    assert brand_in_db.auth_user_id == test_auth_id
    assert data_manager.received('commit', 1)


def test_db_write_new_brand_for_auth_user_when_image_error_occurs():
    image_repo = MockImageRepo({"upload": ImageException()})
    [data_manager, payload] = setup_data("test bytes")
    try:
        db_write_new_brand_for_auth_user(auth_user_id="test auth id",
                                         payload=payload,
                                         data_manager=data_manager,
                                         image_repository=image_repo)
        assert False
    except ImageException:
        assert data_manager.received('rollback', 1)


def test_db_write_new_brand_for_auth_user_when_brand_already_exists_for_auth_user():
    image_repo = MockImageRepo()
    [data_manager, payload] = setup_data("test bytes")
    auth_id = "testid"
    data_manager.create_fake_data([brand_generator(1, auth_id)])
    try:
        db_write_new_brand_for_auth_user(auth_user_id=auth_id,
                                         payload=payload,
                                         data_manager=data_manager,
                                         image_repository=image_repo)
        assert False
    except AlreadyExistsException:
        # nothing to rollback
        pass


def setup_data(bytes_):
    data_manager = InMemorySqliteDataManager()
    payload = {
        "name": "testname",
        "description": "testdescription",
        "website": "testwebsite",
        "email": "testemail",
        "instahandle": "instahandle",
        "image_bytes": bytes_
    }
    return [data_manager, payload]
