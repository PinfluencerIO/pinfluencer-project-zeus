from src.data_access_layer.brand import Brand
from src.data_access_layer.write_data_access import db_write_update_brand_for_auth_user, NoBrandForAuthenticatedUser
from tests import InMemorySqliteDataManager, MockImageRepo, brand_generator


def test_db_write_update_brand_for_auth_user_when_successful():
    [data_manager, image_repository, auth_id, payload] = setup()
    data_manager.create_fake_data([brand_generator(1, auth_id)])
    db_write_update_brand_for_auth_user(auth_user_id=auth_id,
                                        data_manager=data_manager,
                                        image_repository=image_repository,
                                        payload=payload)
    brand_in_db = data_manager.session.query(Brand).first()
    assert brand_in_db.name == payload['name']
    assert brand_in_db.description == payload['description']
    assert brand_in_db.website == payload['website']
    assert brand_in_db.instahandle == payload['instahandle']


def test_db_write_update_brand_for_auth_user_when_brand_doesnt_exist():
    [data_manager, image_repository, auth_id, payload] = setup()
    try:
        db_write_update_brand_for_auth_user(auth_user_id=auth_id,
                                            data_manager=data_manager,
                                            image_repository=image_repository,
                                            payload=payload)
        assert False
    except NoBrandForAuthenticatedUser:
        pass


def setup():
    data_manager = InMemorySqliteDataManager()
    image_repository = MockImageRepo()
    auth_id = "authid"
    payload = {
        "name": "testname",
        "description": "testdescription",
        "website": "testwebsite",
        "instahandle": "instahandle"
    }
    return [data_manager, image_repository, auth_id, payload]
