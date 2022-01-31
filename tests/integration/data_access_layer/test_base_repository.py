from src.data_access_layer.repositories import BrandRepository
from tests import InMemorySqliteDataManager, brand_generator, brand_dto_generator


def test_load_brand_by_id_item_when_brand_can_be_found():
    [data_manager, unexpected_brand] = setup_database()
    repository = BrandRepository(data_manager=data_manager, image_repository=None)
    actual_brand = repository.load_by_id(id_=unexpected_brand.id)
    assert unexpected_brand.__dict__ == actual_brand.__dict__


def test_load_brand_item_by_id_when_brand_cannot_be_found():
    [data_manager, _] = setup_database()
    repository = BrandRepository(data_manager=data_manager, image_repository=None)
    actual_brand = repository.load_by_id(id_="1234")
    assert actual_brand is None


def setup_database():
    data_manager = InMemorySqliteDataManager()
    brand = brand_dto_generator(1)
    data_manager.create_fake_data([brand_generator(brand)])
    return [data_manager, brand]
