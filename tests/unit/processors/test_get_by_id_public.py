import uuid
from unittest.mock import Mock, MagicMock

from src.routes import BrandController
from tests import brand_dto_generator


def test_public_get_by_id_for_brand():
    mock_repository = Mock()
    brand = brand_dto_generator(num=1)
    mock_repository.load_by_id = MagicMock(return_value=brand)
    controller = BrandController(brand_repository=mock_repository, data_manager=None, image_repo=None)
    pinfluencer_response = controller.handle_get_by_id({'pathParameters': {'brand_id': brand.id}})
    mock_repository.load_by_id.assert_called_once_with(id_=brand.id)
    assert pinfluencer_response.body == brand.__dict__
    assert pinfluencer_response.is_ok() is True


def test_public_get_by_id_for_brand_not_found():
    mock_repository = Mock()
    mock_repository.load_by_id = MagicMock(return_value=None)
    controller = BrandController(brand_repository=mock_repository, data_manager=None, image_repo=None)
    field = str(uuid.uuid4())
    pinfluencer_response = controller.handle_get_by_id({'pathParameters': {'brand_id': field}})
    mock_repository.load_by_id.assert_called_once_with(id_=field)
    assert pinfluencer_response.body == {}
    assert pinfluencer_response.status_code == 404


def test_public_get_by_id_for_brand_invalid_uuid():
    mock_repository = Mock()
    mock_repository.load_by_id = MagicMock(return_value=None)
    controller = BrandController(brand_repository=mock_repository, data_manager=None, image_repo=None)
    field = "12345"
    pinfluencer_response = controller.handle_get_by_id({'pathParameters': {'brand_id': field}})
    mock_repository.load_by_id.assert_not_called()
    assert pinfluencer_response.body == {}
    assert pinfluencer_response.status_code == 404
