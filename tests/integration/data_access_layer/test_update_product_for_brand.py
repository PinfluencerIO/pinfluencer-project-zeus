from src.data_access_layer.write_data_access import db_write_update_product_for_auth_user, NotFoundException, \
    NoBrandForAuthenticatedUser
from tests import brand_generator, MockImageRepo, InMemorySqliteDataManager, product_generator


def test_db_write_update_product_for_auth_user_when_successful():
    data_manager = InMemorySqliteDataManager()
    image_repository = MockImageRepo()
    auth_id = "authid"
    brand = brand_generator(1, auth_user_id=auth_id)
    product = product_generator(1, brand=brand)
    payload = {
        "name": "testname",
        "description": "testdescription",
        "requirements": "tag1, tag2",
        "product_id": product.id
    }
    data_manager.create_fake_data([brand])
    data_manager.create_fake_data([product])
    brand_in_db = db_write_update_product_for_auth_user(auth_user_id=auth_id,
                                                        data_manager=data_manager,
                                                        image_repository=image_repository,
                                                        payload=payload)
    assert brand_in_db.name == payload['name']
    assert brand_in_db.description == payload['description']
    assert brand_in_db.requirements == payload['requirements']
    assert data_manager.changes_were_committed_once()


def test_db_write_update_product_for_auth_user_when_brand_doesnt_exist():
    data_manager = InMemorySqliteDataManager()
    image_repository = MockImageRepo()
    try:
        db_write_update_product_for_auth_user(auth_user_id="testid",
                                              data_manager=data_manager,
                                              image_repository=image_repository,
                                              payload={})
        assert False
    except NoBrandForAuthenticatedUser:
        pass
    assert data_manager.no_changes_were_rolled_back_or_committed()


def test_db_write_update_product_for_auth_user_when_product_doesnt_exist():
    data_manager = InMemorySqliteDataManager()
    auth_user_id = "testid"
    data_manager.create_fake_data([brand_generator(1, auth_user_id=auth_user_id)])
    image_repository = MockImageRepo()
    try:
        db_write_update_product_for_auth_user(auth_user_id=auth_user_id,
                                              data_manager=data_manager,
                                              image_repository=image_repository,
                                              payload={"product_id": "testid"})
        assert False
    except NotFoundException:
        pass
    assert data_manager.no_changes_were_rolled_back_or_committed()
