import uuid

from src.data_access_layer.brand import Brand


def mock_load_brand_by_auth_id(auth_id, data_manager):
    brand = Brand()
    brand.id = str(uuid.uuid4())
    return brand


def mock_failed_to_load_brand_by_auth_id(auth_id, data_manager):
    return None
