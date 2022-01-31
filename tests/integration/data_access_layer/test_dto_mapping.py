from src.data_access_layer.entities import BrandEntity
from tests import brand_dto_generator


def test_entity_is_created_in_db_from_dto():
    expected = brand_dto_generator(num=1)
    actual = BrandEntity.create_from_dto(dto=expected).as_dto()
    assert expected.__dict__ == actual.__dict__
