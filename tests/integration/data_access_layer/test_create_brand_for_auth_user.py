from src.data_access_layer.brand import Brand
from src.data_access_layer.write_data_access import db_write_new_brand_for_auth_user
from tests import InMemorySqliteDataManager, SpyImageRepo


def test_db_write_new_brand_for_auth_user_when_record_is_written_successfully():
    test_image = "test.png"
    image_repo = SpyImageRepo({"upload": test_image})
    data_manager = InMemorySqliteDataManager()
    bytes_ = "test bytes"
    test_auth_id = "test auth id"
    payload = payload = {
        "name": "testname",
        "description": "testdescription",
        "website": "testwebsite",
        "email": "testemail",
        "instahandle": "instahandle",
        "image": bytes_
    }
    db_write_new_brand_for_auth_user(auth_user_id=test_auth_id,
                                     payload=payload,
                                     data_manager=data_manager,
                                     image_repository=image_repo)
    brand_in_db = data_manager.session.query(Brand).first()
    assert image_repo.received('upload', 1) and image_repo.received_with_args('upload', [f'{brand_in_db.id}', bytes_])
    assert brand_in_db.name == payload['name']
    assert brand_in_db.description == payload['description']
    assert brand_in_db.website == payload['website']
    assert brand_in_db.email == payload['email']
    assert brand_in_db.instahandle == payload['instahandle']
    assert brand_in_db.image == test_image
    assert brand_in_db.auth_user_id == test_auth_id
