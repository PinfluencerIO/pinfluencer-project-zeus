from src.data_access_layer.brand import Brand
from src.data_access_layer.write_data_access import db_write_new_brand_for_auth_user
from tests import InMemorySqliteDataManager, SpyImageRepo


def test_db_write_new_brand_for_auth_user_when_record_is_written_successfully():
    image_repo = SpyImageRepo({"upload": "test"})
    data_manager = InMemorySqliteDataManager()
    bytes_ = "test bytes"
    db_write_new_brand_for_auth_user(auth_user_id="",
                                     payload={
                                         "name": "testname",
                                         "description": "testdescription",
                                         "website": "testwebsite",
                                         "email": "testemail",
                                         "instahandle": "instahandle",
                                         "image": bytes_
                                     },
                                     data_manager=data_manager,
                                     image_repository=image_repo)
    assert image_repo.received('upload') == 1 and image_repo.with_args('upload') == [
        f'{data_manager.session.query(Brand).first().id}', bytes_]
