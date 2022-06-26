from unittest import TestCase

from mapper.object_mapper import ObjectMapper

from src.data.entities import create_mappings, SqlAlchemyBrandEntity, SqlAlchemyInfluencerEntity
from src.domain.models import Brand, Influencer
from tests import brand_dto_generator, get_entity_dict, influencer_dto_generator, assert_brand_db_fields_are_equal, \
    assert_influencer_db_fields_are_equal


class TestMappings(TestCase):

    def setUp(self) -> None:
        self._mapper = ObjectMapper()
        create_mappings(mapper=self._mapper)


class TestBrandMappings(TestMappings):

    def test_map_brand_to_brand_entity(self):

        # arrange
        brand = brand_dto_generator(num=1)

        # act
        brand_entity = self._mapper.map(from_obj=brand, to_type=SqlAlchemyBrandEntity)

        # assert
        assert_brand_db_fields_are_equal(brand1=brand.__dict__, brand2=get_entity_dict(brand_entity))

    def test_map_brand_entity_to_brand(self):

        # arrange
        brand = brand_dto_generator(num=1)

        # act
        brand_entity = self._mapper.map(from_obj=brand, to_type=SqlAlchemyBrandEntity)
        brand_mapped_back = self._mapper.map(from_obj=brand_entity, to_type=Brand)

        # assert
        assert_brand_db_fields_are_equal(brand1=brand.__dict__, brand2=brand_mapped_back.__dict__)


class TestInfluencerMappings(TestMappings):

    def test_map_influencer_to_influencer_entity(self):

        # arrange
        influencer = influencer_dto_generator(num=1)

        # act
        influencer_entity = self._mapper.map(from_obj=influencer, to_type=SqlAlchemyInfluencerEntity)

        # assert
        assert_influencer_db_fields_are_equal(influencer1=influencer.__dict__, influencer2=get_entity_dict(influencer_entity))

    def test_map_influencer_entity_to_influencer(self):

        # arrange
        influencer = influencer_dto_generator(num=1)

        # act
        influencer_entity = self._mapper.map(from_obj=influencer, to_type=SqlAlchemyInfluencerEntity)
        influencer_mapped_back = self._mapper.map(from_obj=influencer_entity, to_type=Influencer)

        # assert
        assert_influencer_db_fields_are_equal(influencer1=influencer.__dict__, influencer2=influencer_mapped_back.__dict__)
