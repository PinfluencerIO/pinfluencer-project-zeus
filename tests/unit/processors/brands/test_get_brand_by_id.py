import uuid

from src.data_access_layer.brand import Brand
from src.filters import FilterResponse
from src.processors.brands.get_brands_by_id import ProcessPublicGetBrandBy
from tests.unit.processors.brands import MockFilterResponse


def test_process_successful_public_get_brand_by_id():
    b = Brand()
    b.id = str(uuid.uuid4())
    mock_load_resource = MockFilterResponse(response=FilterResponse('', 200, b.as_dict()))
    processor = ProcessPublicGetBrandBy(mock_load_resource)
    pinfluencer_response = processor.do_process(
        {'pathParameters': {'brand_id': b.id}})
    assert pinfluencer_response.is_ok() is True
    assert pinfluencer_response.body == b.as_dict()


def test_process_unsuccessful_public_get_brand_by_id():
    b = Brand()
    b.id = str(uuid.uuid4())
    mock_load_resource_that_failed = MockFilterResponse(response=FilterResponse('', 400, {}))
    processor = ProcessPublicGetBrandBy(mock_load_resource_that_failed)
    pinfluencer_response = processor.do_process(
        {'pathParameters': {'brand_id': b.id}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400
