from unittest import TestCase

from src.crosscutting import AutoFixture
from src.domain.models import Brand, Influencer, Campaign
from src.web.mapping import MappingRules
from src.web.views import BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto, \
    CampaignResponseDto, CampaignRequestDto
from tests import test_mapper


class TestMappingRules(TestCase):

    def setUp(self) -> None:
        self.__mapper = test_mapper()
        self.__sut = MappingRules(mapper=self.__mapper)
        self.__fixture = AutoFixture()

    def test_map_brand_to_brand_request(self):
        # arrange
        brand = self.__fixture.create(dto=Brand, list_limit=5)

        self.__sut.add_rules()

        # act
        brand_request = self.__mapper.map(_from=brand, to=BrandRequestDto)

        # assert
        with self.subTest(msg="brand name matches"):
            self.assertEqual(brand_request.brand_name, brand.brand_name)

        # assert
        with self.subTest(msg="brand description matches"):
            self.assertEqual(brand_request.brand_description, brand.brand_description)

        # assert
        with self.subTest(msg="brand values match"):
            self.assertEqual(brand_request.values, list(map(lambda x: x.value, brand.values)))

        # assert
        with self.subTest(msg="brand categories match"):
            self.assertEqual(brand_request.categories, list(map(lambda x: x.category, brand.categories)))

        # assert
        with self.subTest(msg="brand website matches"):
            self.assertEqual(brand_request.website, brand.website)

        # assert
        with self.subTest(msg="brand insta handle matches"):
            self.assertEqual(brand_request.insta_handle, brand.insta_handle)

    def test_map_brand_request_to_brand(self):
        # arrange
        brand_request = self.__fixture.create(dto=BrandRequestDto, list_limit=5)

        self.__sut.add_rules()

        # act
        brand = self.__mapper.map(_from=brand_request, to=Brand)

        # assert
        with self.subTest(msg="brand name matches"):
            self.assertEqual(brand.brand_name, brand_request.brand_name)

        # assert
        with self.subTest(msg="brand description matches"):
            self.assertEqual(brand.brand_description, brand_request.brand_description)

        # assert
        with self.subTest(msg="brand values match"):
            self.assertEqual(list(map(lambda x: x.value, brand.values)), brand_request.values)

        # assert
        with self.subTest(msg="brand categories match"):
            self.assertEqual(list(map(lambda x: x.category, brand.categories)), brand_request.categories)

        # assert
        with self.subTest(msg="brand website matches"):
            self.assertEqual(brand.website, brand_request.website)

        # assert
        with self.subTest(msg="brand insta handle matches"):
            self.assertEqual(brand.insta_handle, brand_request.insta_handle)

    def test_map_brand_to_brand_response(self):
        # arrange
        brand = self.__fixture.create(dto=Brand, list_limit=5)

        self.__sut.add_rules()

        # act
        brand_response = self.__mapper.map(_from=brand, to=BrandResponseDto)

        # assert
        with self.subTest(msg="brand id matches"):
            self.assertEqual(brand_response.id, brand.id)

        # assert
        with self.subTest(msg="brand created date matches"):
            self.assertEqual(brand_response.created, brand.created)

        # assert
        with self.subTest(msg="brand auth user id matches"):
            self.assertEqual(brand_response.auth_user_id, brand.auth_user_id)

        # assert
        with self.subTest(msg="brand name matches"):
            self.assertEqual(brand_response.brand_name, brand.brand_name)

        # assert
        with self.subTest(msg="brand description matches"):
            self.assertEqual(brand_response.brand_description, brand.brand_description)

        # assert
        with self.subTest(msg="brand values match"):
            self.assertEqual(brand_response.values, list(map(lambda x: x.value, brand.values)))

        # assert
        with self.subTest(msg="brand categories match"):
            self.assertEqual(brand_response.categories, list(map(lambda x: x.category, brand.categories)))

        # assert
        with self.subTest(msg="brand website matches"):
            self.assertEqual(brand_response.website, brand.website)

        # assert
        with self.subTest(msg="brand insta handle matches"):
            self.assertEqual(brand_response.insta_handle, brand.insta_handle)

    def test_map_brand_response_to_brand(self):
        # arrange
        brand_response = self.__fixture.create(dto=BrandResponseDto, list_limit=5)

        self.__sut.add_rules()

        # act
        brand = self.__mapper.map(_from=brand_response, to=Brand)

        # assert
        with self.subTest(msg="brand id matches"):
            self.assertEqual(brand_response.id, brand.id)

        # assert
        with self.subTest(msg="brand created date matches"):
            self.assertEqual(brand_response.created, brand.created)

        # assert
        with self.subTest(msg="brand auth user id matches"):
            self.assertEqual(brand_response.auth_user_id, brand.auth_user_id)

        # assert
        with self.subTest(msg="brand name matches"):
            self.assertEqual(brand.brand_name, brand_response.brand_name)

        # assert
        with self.subTest(msg="brand description matches"):
            self.assertEqual(brand.brand_description, brand_response.brand_description)

        # assert
        with self.subTest(msg="brand values match"):
            self.assertEqual(list(map(lambda x: x.value, brand.values)), brand_response.values)

        # assert
        with self.subTest(msg="brand categories match"):
            self.assertEqual(list(map(lambda x: x.category, brand.categories)), brand_response.categories)

        # assert
        with self.subTest(msg="brand website matches"):
            self.assertEqual(brand.website, brand_response.website)

        # assert
        with self.subTest(msg="brand insta handle matches"):
            self.assertEqual(brand.insta_handle, brand_response.insta_handle)
            
    def test_map_influencer_to_influencer_request(self):
        # arrange
        influencer = AutoFixture().create(dto=Influencer, list_limit=5)
        
        # act
        self.__sut.add_rules()
        influencer_request = self.__mapper.map(_from=influencer, to=InfluencerRequestDto)
        
        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(influencer_request.values, list(map(lambda x: x.value, influencer.values)))

        # assert
        with self.subTest(msg="websites match"):
            self.assertEqual(influencer_request.website, influencer.website)
            
        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(influencer_request.categories, list(map(lambda x: x.category, influencer.categories)))

        # assert
        with self.subTest(msg="insta handles match"):
            self.assertEqual(influencer_request.insta_handle, influencer.insta_handle)

        # assert
        with self.subTest(msg="bios match"):
            self.assertEqual(influencer_request.bio, influencer.bio)

        # assert
        with self.subTest(msg="audience_male_splits match"):
            self.assertEqual(influencer_request.audience_male_split, influencer.audience_male_split)

        # assert
        with self.subTest(msg="audience_female_splits match"):
            self.assertEqual(influencer_request.audience_female_split, influencer.audience_female_split)

        # assert
        with self.subTest(msg="audience_age_65_plus_splits match"):
            self.assertEqual(influencer_request.audience_age_65_plus_split, influencer.audience_age_65_plus_split)

        # assert
        with self.subTest(msg="audience_age_55_to_64_splits match"):
            self.assertEqual(influencer_request.audience_age_55_to_64_split, influencer.audience_age_55_to_64_split)

        # assert
        with self.subTest(msg="audience_age_45_to_54_splits match"):
            self.assertEqual(influencer_request.audience_age_45_to_54_split, influencer.audience_age_45_to_54_split)

        # assert
        with self.subTest(msg="audience_age_35_to_44_splits match"):
            self.assertEqual(influencer_request.audience_age_35_to_44_split, influencer.audience_age_35_to_44_split)

        # assert
        with self.subTest(msg="audience_age_25_to_34_splits match"):
            self.assertEqual(influencer_request.audience_age_25_to_34_split, influencer.audience_age_25_to_34_split)

        # assert
        with self.subTest(msg="audience_age_18_to_24_splits match"):
            self.assertEqual(influencer_request.audience_age_18_to_24_split, influencer.audience_age_18_to_24_split)

        # assert
        with self.subTest(msg="audience_age_13_to_17_splits match"):
            self.assertEqual(influencer_request.audience_age_13_to_17_split, influencer.audience_age_13_to_17_split)

        # assert
        with self.subTest(msg="addresses match"):
            self.assertEqual(influencer_request.address, influencer.address)

    def test_map_influencer_request_to_influencer(self):
        # arrange
        influencer_request = AutoFixture().create(dto=InfluencerRequestDto, list_limit=5)

        # act
        self.__sut.add_rules()
        influencer = self.__mapper.map(_from=influencer_request, to=Influencer)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(influencer_request.values, list(map(lambda x: x.value, influencer.values)))

        # assert
        with self.subTest(msg="websites match"):
            self.assertEqual(influencer_request.website, influencer.website)

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(influencer_request.categories, list(map(lambda x: x.category, influencer.categories)))

        # assert
        with self.subTest(msg="insta handles match"):
            self.assertEqual(influencer_request.insta_handle, influencer.insta_handle)

        # assert
        with self.subTest(msg="bios match"):
            self.assertEqual(influencer_request.bio, influencer.bio)

        # assert
        with self.subTest(msg="audience_male_splits match"):
            self.assertEqual(influencer_request.audience_male_split, influencer.audience_male_split)

        # assert
        with self.subTest(msg="audience_female_splits match"):
            self.assertEqual(influencer_request.audience_female_split, influencer.audience_female_split)

        # assert
        with self.subTest(msg="audience_age_65_plus_splits match"):
            self.assertEqual(influencer_request.audience_age_65_plus_split, influencer.audience_age_65_plus_split)

        # assert
        with self.subTest(msg="audience_age_55_to_64_splits match"):
            self.assertEqual(influencer_request.audience_age_55_to_64_split, influencer.audience_age_55_to_64_split)

        # assert
        with self.subTest(msg="audience_age_45_to_54_splits match"):
            self.assertEqual(influencer_request.audience_age_45_to_54_split, influencer.audience_age_45_to_54_split)

        # assert
        with self.subTest(msg="audience_age_35_to_44_splits match"):
            self.assertEqual(influencer_request.audience_age_35_to_44_split, influencer.audience_age_35_to_44_split)

        # assert
        with self.subTest(msg="audience_age_25_to_34_splits match"):
            self.assertEqual(influencer_request.audience_age_25_to_34_split, influencer.audience_age_25_to_34_split)

        # assert
        with self.subTest(msg="audience_age_18_to_24_splits match"):
            self.assertEqual(influencer_request.audience_age_18_to_24_split, influencer.audience_age_18_to_24_split)

        # assert
        with self.subTest(msg="audience_age_13_to_17_splits match"):
            self.assertEqual(influencer_request.audience_age_13_to_17_split, influencer.audience_age_13_to_17_split)

        # assert
        with self.subTest(msg="addresses match"):
            self.assertEqual(influencer_request.address, influencer.address)

    def test_map_influencer_to_influencer_response(self):
        # arrange
        influencer = AutoFixture().create(dto=Influencer, list_limit=5)

        # act
        self.__sut.add_rules()
        influencer_response = self.__mapper.map(_from=influencer, to=InfluencerResponseDto)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(influencer_response.values, list(map(lambda x: x.value, influencer.values)))

        # assert
        with self.subTest(msg="websites match"):
            self.assertEqual(influencer_response.website, influencer.website)

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(influencer_response.categories, list(map(lambda x: x.category, influencer.categories)))

        # assert
        with self.subTest(msg="insta handles match"):
            self.assertEqual(influencer_response.insta_handle, influencer.insta_handle)

        # assert
        with self.subTest(msg="bios match"):
            self.assertEqual(influencer_response.bio, influencer.bio)

        # assert
        with self.subTest(msg="auth user ids match"):
            self.assertEqual(influencer_response.auth_user_id, influencer.auth_user_id)

        # assert
        with self.subTest(msg="images match"):
            self.assertEqual(influencer_response.image, influencer.image)

        # assert
        with self.subTest(msg="ids match"):
            self.assertEqual(influencer_response.id, influencer.id)

        # assert
        with self.subTest(msg="created dates match"):
            self.assertEqual(influencer_response.created, influencer.created)

        # assert
        with self.subTest(msg="audience_male_splits match"):
            self.assertEqual(influencer_response.audience_male_split, influencer.audience_male_split)

        # assert
        with self.subTest(msg="audience_female_splits match"):
            self.assertEqual(influencer_response.audience_female_split, influencer.audience_female_split)

        # assert
        with self.subTest(msg="audience_age_65_plus_splits match"):
            self.assertEqual(influencer_response.audience_age_65_plus_split, influencer.audience_age_65_plus_split)

        # assert
        with self.subTest(msg="audience_age_55_to_64_splits match"):
            self.assertEqual(influencer_response.audience_age_55_to_64_split, influencer.audience_age_55_to_64_split)

        # assert
        with self.subTest(msg="audience_age_45_to_54_splits match"):
            self.assertEqual(influencer_response.audience_age_45_to_54_split, influencer.audience_age_45_to_54_split)

        # assert
        with self.subTest(msg="audience_age_35_to_44_splits match"):
            self.assertEqual(influencer_response.audience_age_35_to_44_split, influencer.audience_age_35_to_44_split)

        # assert
        with self.subTest(msg="audience_age_25_to_34_splits match"):
            self.assertEqual(influencer_response.audience_age_25_to_34_split, influencer.audience_age_25_to_34_split)

        # assert
        with self.subTest(msg="audience_age_18_to_24_splits match"):
            self.assertEqual(influencer_response.audience_age_18_to_24_split, influencer.audience_age_18_to_24_split)

        # assert
        with self.subTest(msg="audience_age_13_to_17_splits match"):
            self.assertEqual(influencer_response.audience_age_13_to_17_split, influencer.audience_age_13_to_17_split)

        # assert
        with self.subTest(msg="addresses match"):
            self.assertEqual(influencer_response.address, influencer.address)

    def test_map_influencer_response_to_influencer(self):
        # arrange
        influencer_response = AutoFixture().create(dto=InfluencerResponseDto, list_limit=5)

        # act
        self.__sut.add_rules()
        influencer = self.__mapper.map(_from=influencer_response, to=Influencer)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(influencer_response.values, list(map(lambda x: x.value, influencer.values)))

        # assert
        with self.subTest(msg="websites match"):
            self.assertEqual(influencer_response.website, influencer.website)

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(influencer_response.categories, list(map(lambda x: x.category, influencer.categories)))

        # assert
        with self.subTest(msg="insta handles match"):
            self.assertEqual(influencer_response.insta_handle, influencer.insta_handle)

        # assert
        with self.subTest(msg="bios match"):
            self.assertEqual(influencer_response.bio, influencer.bio)

        # assert
        with self.subTest(msg="auth user ids match"):
            self.assertEqual(influencer_response.auth_user_id, influencer.auth_user_id)

        # assert
        with self.subTest(msg="images match"):
            self.assertEqual(influencer_response.image, influencer.image)

        # assert
        with self.subTest(msg="ids match"):
            self.assertEqual(influencer_response.id, influencer.id)

        # assert
        with self.subTest(msg="created dates match"):
            self.assertEqual(influencer_response.created, influencer.created)

        # assert
        with self.subTest(msg="audience_male_splits match"):
            self.assertEqual(influencer_response.audience_male_split, influencer.audience_male_split)

        # assert
        with self.subTest(msg="audience_female_splits match"):
            self.assertEqual(influencer_response.audience_female_split, influencer.audience_female_split)

        # assert
        with self.subTest(msg="audience_age_65_plus_splits match"):
            self.assertEqual(influencer_response.audience_age_65_plus_split, influencer.audience_age_65_plus_split)

        # assert
        with self.subTest(msg="audience_age_55_to_64_splits match"):
            self.assertEqual(influencer_response.audience_age_55_to_64_split, influencer.audience_age_55_to_64_split)

        # assert
        with self.subTest(msg="audience_age_45_to_54_splits match"):
            self.assertEqual(influencer_response.audience_age_45_to_54_split, influencer.audience_age_45_to_54_split)

        # assert
        with self.subTest(msg="audience_age_35_to_44_splits match"):
            self.assertEqual(influencer_response.audience_age_35_to_44_split, influencer.audience_age_35_to_44_split)

        # assert
        with self.subTest(msg="audience_age_25_to_34_splits match"):
            self.assertEqual(influencer_response.audience_age_25_to_34_split, influencer.audience_age_25_to_34_split)

        # assert
        with self.subTest(msg="audience_age_18_to_24_splits match"):
            self.assertEqual(influencer_response.audience_age_18_to_24_split, influencer.audience_age_18_to_24_split)

        # assert
        with self.subTest(msg="audience_age_13_to_17_splits match"):
            self.assertEqual(influencer_response.audience_age_13_to_17_split, influencer.audience_age_13_to_17_split)

        # assert
        with self.subTest(msg="addresses match"):
            self.assertEqual(influencer_response.address, influencer.address)

    def test_map_campaign_to_campaign_response(self):
        # arrange
        campaign = AutoFixture().create(dto=Campaign, list_limit=5)

        # act
        self.__sut.add_rules()
        campaign_response = self.__mapper.map(_from=campaign, to=CampaignResponseDto)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(campaign_response.campaign_values, list(map(lambda x: x.value, campaign.campaign_values)))

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(campaign_response.campaign_categories, list(map(lambda x: x.category, campaign.campaign_categories)))

        # assert
        with self.subTest(msg="ids match"):
            self.assertEqual(campaign_response.id, campaign.id)

        # assert
        with self.subTest(msg="created dates match"):
            self.assertEqual(campaign_response.created, campaign.created)

        # assert
        with self.subTest(msg="hashtag match"):
            self.assertEqual(campaign_response.campaign_hashtag, campaign.campaign_hashtag)

        # assert
        with self.subTest(msg="product image match"):
            self.assertEqual(campaign_response.product_image, campaign.product_image)

        # assert
        with self.subTest(msg="product links match"):
            self.assertEqual(campaign_response.campaign_product_link, campaign.campaign_product_link)

        # assert
        with self.subTest(msg="campaign states match"):
            self.assertEqual(campaign_response.campaign_state, campaign.campaign_state)

        # assert
        with self.subTest(msg="discount codes match"):
            self.assertEqual(campaign_response.campaign_discount_code, campaign.campaign_discount_code)

        # assert
        with self.subTest(msg="objectives match"):
            self.assertEqual(campaign_response.objective, campaign.objective)

        # assert
        with self.subTest(msg="product descriptions match"):
            self.assertEqual(campaign_response.product_description, campaign.product_description)

        # assert
        with self.subTest(msg="product titles match"):
            self.assertEqual(campaign_response.product_title, campaign.product_title)

        # assert
        with self.subTest(msg="success descriptions match"):
            self.assertEqual(campaign_response.success_description, campaign.success_description)

        # assert
        with self.subTest(msg="campaign titles match"):
            self.assertEqual(campaign_response.campaign_title, campaign.campaign_title)

        # assert
        with self.subTest(msg="brand auth user ids match"):
            self.assertEqual(campaign_response.brand_auth_user_id, campaign.brand_auth_user_id)

        # assert
        with self.subTest(msg="campaign descriptions match"):
            self.assertEqual(campaign_response.campaign_description, campaign.campaign_description)

    def test_map_campaign_response_to_campaign(self):
        # arrange
        campaign_response = AutoFixture().create(dto=CampaignResponseDto, list_limit=5)

        # act
        self.__sut.add_rules()
        campaign = self.__mapper.map(_from=campaign_response, to=Campaign)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(campaign_response.campaign_values, list(map(lambda x: x.value, campaign.campaign_values)))

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(campaign_response.campaign_categories, list(map(lambda x: x.category, campaign.campaign_categories)))

        # assert
        with self.subTest(msg="ids match"):
            self.assertEqual(campaign_response.id, campaign.id)

        # assert
        with self.subTest(msg="created dates match"):
            self.assertEqual(campaign_response.created, campaign.created)

        # assert
        with self.subTest(msg="hashtag match"):
            self.assertEqual(campaign_response.campaign_hashtag, campaign.campaign_hashtag)

        # assert
        with self.subTest(msg="product image match"):
            self.assertEqual(campaign_response.product_image, campaign.product_image)

        # assert
        with self.subTest(msg="product links match"):
            self.assertEqual(campaign_response.campaign_product_link, campaign.campaign_product_link)

        # assert
        with self.subTest(msg="campaign states match"):
            self.assertEqual(campaign_response.campaign_state, campaign.campaign_state)

        # assert
        with self.subTest(msg="discount codes match"):
            self.assertEqual(campaign_response.campaign_discount_code, campaign.campaign_discount_code)

        # assert
        with self.subTest(msg="objectives match"):
            self.assertEqual(campaign_response.objective, campaign.objective)

        # assert
        with self.subTest(msg="product descriptions match"):
            self.assertEqual(campaign_response.product_description, campaign.product_description)

        # assert
        with self.subTest(msg="product titles match"):
            self.assertEqual(campaign_response.product_title, campaign.product_title)

        # assert
        with self.subTest(msg="success descriptions match"):
            self.assertEqual(campaign_response.success_description, campaign.success_description)

        # assert
        with self.subTest(msg="campaign titles match"):
            self.assertEqual(campaign_response.campaign_title, campaign.campaign_title)

        # assert
        with self.subTest(msg="brand auth user ids match"):
            self.assertEqual(campaign_response.brand_auth_user_id, campaign.brand_auth_user_id)

        # assert
        with self.subTest(msg="campaign descriptions match"):
            self.assertEqual(campaign_response.campaign_description, campaign.campaign_description)

    def test_map_campaign_to_campaign_request(self):
        # arrange
        campaign = AutoFixture().create(dto=Campaign, list_limit=5)

        # act
        self.__sut.add_rules()
        campaign_request = self.__mapper.map(_from=campaign, to=CampaignRequestDto)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(campaign_request.campaign_values, list(map(lambda x: x.value, campaign.campaign_values)))

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(campaign_request.campaign_categories, list(map(lambda x: x.category, campaign.campaign_categories)))


        # assert
        with self.subTest(msg="hashtag match"):
            self.assertEqual(campaign_request.campaign_hashtag, campaign.campaign_hashtag)


        # assert
        with self.subTest(msg="product links match"):
            self.assertEqual(campaign_request.campaign_product_link, campaign.campaign_product_link)

        # assert
        with self.subTest(msg="campaign states match"):
            self.assertEqual(campaign_request.campaign_state, campaign.campaign_state)

        # assert
        with self.subTest(msg="discount codes match"):
            self.assertEqual(campaign_request.campaign_discount_code, campaign.campaign_discount_code)

        # assert
        with self.subTest(msg="objectives match"):
            self.assertEqual(campaign_request.objective, campaign.objective)

        # assert
        with self.subTest(msg="product descriptions match"):
            self.assertEqual(campaign_request.product_description, campaign.product_description)

        # assert
        with self.subTest(msg="product titles match"):
            self.assertEqual(campaign_request.product_title, campaign.product_title)

        # assert
        with self.subTest(msg="success descriptions match"):
            self.assertEqual(campaign_request.success_description, campaign.success_description)

        # assert
        with self.subTest(msg="campaign titles match"):
            self.assertEqual(campaign_request.campaign_title, campaign.campaign_title)

        # assert
        with self.subTest(msg="campaign descriptions match"):
            self.assertEqual(campaign_request.campaign_description, campaign.campaign_description)

    def test_map_campaign_request_to_campaign(self):
        # arrange
        campaign_request = AutoFixture().create(dto=CampaignRequestDto, list_limit=5)

        # act
        self.__sut.add_rules()
        campaign = self.__mapper.map(_from=campaign_request, to=Campaign)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(campaign_request.campaign_values, list(map(lambda x: x.value, campaign.campaign_values)))

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(campaign_request.campaign_categories, list(map(lambda x: x.category, campaign.campaign_categories)))


        # assert
        with self.subTest(msg="hashtag match"):
            self.assertEqual(campaign_request.campaign_hashtag, campaign.campaign_hashtag)


        # assert
        with self.subTest(msg="product links match"):
            self.assertEqual(campaign_request.campaign_product_link, campaign.campaign_product_link)

        # assert
        with self.subTest(msg="campaign states match"):
            self.assertEqual(campaign_request.campaign_state, campaign.campaign_state)

        # assert
        with self.subTest(msg="discount codes match"):
            self.assertEqual(campaign_request.campaign_discount_code, campaign.campaign_discount_code)

        # assert
        with self.subTest(msg="objectives match"):
            self.assertEqual(campaign_request.objective, campaign.objective)

        # assert
        with self.subTest(msg="product descriptions match"):
            self.assertEqual(campaign_request.product_description, campaign.product_description)

        # assert
        with self.subTest(msg="product titles match"):
            self.assertEqual(campaign_request.product_title, campaign.product_title)

        # assert
        with self.subTest(msg="success descriptions match"):
            self.assertEqual(campaign_request.success_description, campaign.success_description)

        # assert
        with self.subTest(msg="campaign titles match"):
            self.assertEqual(campaign_request.campaign_title, campaign.campaign_title)

        # assert
        with self.subTest(msg="campaign descriptions match"):
            self.assertEqual(campaign_request.campaign_description, campaign.campaign_description)