import uuid
from unittest.mock import Mock, MagicMock

from src.processors.get_by_id import ProcessGetBy
from src.routes import BrandController
from tests import StubDataManager, brand_dto_generator


def test_public_get_by_id_for_brand():
    mock_repository = Mock()
    brand = brand_dto_generator(num=1)
    mock_repository.load_by_id = MagicMock(return_value=brand)
    controller = BrandController(brand_repository=mock_repository, data_manager=None, image_repo=None)
    pinfluencer_response = controller.handle_get_by_id({'pathParameters': {'brand_id': brand.id}})
    mock_repository.load_by_id.assert_called_once_with(id_=brand.id)
    assert pinfluencer_response.body == brand.__dict__
    assert pinfluencer_response.is_ok() is True


def test_process_public_get_by_id_for_brand_not_found():
    mock_repository = Mock()
    mock_repository.load_by_id = MagicMock(return_value=None)
    controller = BrandController(brand_repository=mock_repository, data_manager=None, image_repo=None)
    field = str(uuid.uuid4())
    pinfluencer_response = controller.handle_get_by_id({'pathParameters': {'brand_id': field}})
    mock_repository.load_by_id.assert_called_once_with(id_=field)
    assert pinfluencer_response.body == {}
    assert pinfluencer_response.status_code == 404


def test_process_public_get_by_id_for_brand_invalid_uuid():
    processor = ProcessGetBy(mock_db_load_for_brand, 'brand', StubDataManager())
    pinfluencer_response = processor.do_process({'pathParameters': {'brand_id': '213-123'}})
    assert pinfluencer_response.is_ok() is False
    assert pinfluencer_response.status_code == 400
