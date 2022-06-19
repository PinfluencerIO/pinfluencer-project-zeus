from unittest import TestCase

from mapper.object_mapper import ObjectMapper

from src.data.entities import create_mappings, SqlAlchemyBrandEntity, SqlAlchemyInfluencerEntity
from src.domain.models import Brand, Influencer
from tests import brand_dto_generator, get_entity_dict, influencer_dto_generator


class TestMappings(TestCase):

    def setUp(self) -> None:
        self._mapper = ObjectMapper()
        create_mappings(mapper=self._mapper)


class TestMappings(TestCase):

    def setUp(self) -> None:
        self._mapper = ObjectMapper()
        create_mappings(mapper=self._mapper)


class TestBrandMappings(TestMappings):

    def test_map_brand_to_brand_entity(self):
        brand = brand_dto_generator(num=1)
        brand_entity = self._mapper.map(from_obj=brand, to_type=SqlAlchemyBrandEntity)
        assert brand.__dict__ == get_entity_dict(brand_entity)

    def test_map_brand_entity_to_brand(self):
        brand = brand_dto_generator(num=1)
        brand_entity = self._mapper.map(from_obj=brand, to_type=SqlAlchemyBrandEntity)
        brand_mapped_back = self._mapper.map(from_obj=brand_entity, to_type=Brand)
        assert brand.__dict__ == brand_mapped_back.__dict__


class TestInfluencerMappings(TestMappings):

    def test_map_influencer_to_influencer_entity(self):
        influencer = influencer_dto_generator(num=1)
        influencer_entity = self._mapper.map(from_obj=influencer, to_type=SqlAlchemyInfluencerEntity)
        assert influencer.__dict__ == get_entity_dict(influencer_entity)

    def test_map_influencer_entity_to_influencer(self):
        influencer = influencer_dto_generator(num=1)
        influencer_entity = self._mapper.map(from_obj=influencer, to_type=SqlAlchemyInfluencerEntity)
        influencer_mapped_back = self._mapper.map(from_obj=influencer_entity, to_type=Influencer)
        assert influencer.__dict__ == influencer_mapped_back.__dict__
