from src.data_access_layer.repositories import BrandRepository
from tests import InMemorySqliteDataManager


def test_load_entity_item_when_no_entity_exist():
    data_manager = InMemorySqliteDataManager()
    repository = BrandRepository(data_manager=data_manager, image_repository=None)
    item = repository.load_item()
    assert item == None
