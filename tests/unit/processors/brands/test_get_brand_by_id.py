import uuid

from src.data_access_layer.brand import Brand
from src.filters import FilterResponse
from src.processors.brands.get_brands_by_id import ProcessPublicGetBrandBy
from tests.unit import StubDataManager
from tests.unit.processors.brands import MockFilterResponse

b = Brand()
b.id = str(uuid.uuid4())


def mock_db_load(id, r, data_manager):
    if id == b.id:
        return b
    else:
        return None


def test_process_successful_public_get_brand_by_id():
    processor = ProcessPublicGetBrandBy(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': b.id}})
    assert pinfluencer_response.is_ok() is True
    assert pinfluencer_response.body == b.as_dict()


def test_process_unsuccessful_public_get_brand_by_id():
    processor = ProcessPublicGetBrandBy(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 404


def test_process_unsuccessful_public_get_brand_by_id_invalid_uuid():
    processor = ProcessPublicGetBrandBy(mock_db_load, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': '213-123'}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400
