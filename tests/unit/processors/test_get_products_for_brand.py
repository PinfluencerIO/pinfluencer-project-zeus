import uuid

from src.data_access_layer.brand import Brand
from src.filters import FilterResponse
from src.processors.get_products_for_brand import ProcessPublicAllProductsForBrand
from tests.unit import StubDataManager
from tests.unit.processors.test_brands import MockLoadResourcesId, mock_load_all_products_for_brand_id


def test_process_public_all_products_for_brand():
    b = Brand()
    b.id = str(uuid.uuid4())
    resources_id = MockLoadResourcesId(return_value=FilterResponse('', 200, b.as_dict()))
    processor = ProcessPublicAllProductsForBrand(resources_id, mock_load_all_products_for_brand_id, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is True


def test_process_public_all_products_for_brand_failed_to_load_by_id():
    resources_id = MockLoadResourcesId(return_value=FilterResponse('', 400, {}))
    processor = ProcessPublicAllProductsForBrand(resources_id, mock_load_all_products_for_brand_id, StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': str(uuid.uuid4())}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400
