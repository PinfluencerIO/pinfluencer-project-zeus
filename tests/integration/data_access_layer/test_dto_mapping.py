from src.data_access_layer.repositories import BrandRepository
from tests import InMemorySqliteDataManager, brand_dto_generator, brand_generator


def test_entity_is_created_in_db_from_dto():
    data_manager = InMemorySqliteDataManager()
    brand = brand_dto_generator(num=1)
    data_manager.create_fake_data([brand_generator(dto=brand)])
    repository = BrandRepository(data_manager=data_manager, image_repository=None)
    item = repository.load_item()
    assert brand.__dict__ == item.__dict__