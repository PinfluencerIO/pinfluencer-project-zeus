from src.data_access_layer.write_data_access import db_write_update_brand_for_auth_user, NoBrandForAuthenticatedUser
from tests import InMemorySqliteDataManager, MockImageRepo, brand_generator


def test_db_write_update_brand_for_auth_user_when_successful():
    data_manager = InMemorySqliteDataManager()
    image_repository = MockImageRepo()
    auth_id = "authid"
    payload = {
        "name": "testname",
        "description": "testdescription",
        "website": "testwebsite",
        "instahandle": "instahandle"
    }
    data_manager.create_fake_data([brand_generator(1, auth_id)])
    brand_in_db = db_write_update_brand_for_auth_user(auth_user_id=auth_id,
                                                      data_manager=data_manager,
                                                      image_repository=image_repository,
                                                      payload=payload)
    assert brand_in_db.name == payload['name']
    assert brand_in_db.description == payload['description']
    assert brand_in_db.website == payload['website']
    assert brand_in_db.instahandle == payload['instahandle']
    assert data_manager.changes_were_committed_once()


def test_db_write_update_brand_for_auth_user_when_brand_doesnt_exist():
    data_manager = InMemorySqliteDataManager()
    image_repository = MockImageRepo()
    try:
        db_write_update_brand_for_auth_user(auth_user_id="",
                                            data_manager=data_manager,
                                            image_repository=image_repository,
                                            payload={})
        assert False
    except NoBrandForAuthenticatedUser:
        pass
    assert data_manager.changes_were_rolled_back_once()
