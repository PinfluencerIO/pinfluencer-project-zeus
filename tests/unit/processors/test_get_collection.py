from src.processors.get_collection import ProcessGetCollection
from tests.unit import StubDataManager


def test_do_process_get_collection():
    processor = ProcessGetCollection('brand', mock_load_collection, StubDataManager())
    response = processor.do_process({})
    assert response.is_ok() is True
    assert response.status_code == 200


def mock_load_collection(type, data_manager):
    return []
