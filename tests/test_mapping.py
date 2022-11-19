import datetime
from unittest import TestCase

from ddt import data, ddt

from src.crosscutting import AutoFixture
from src.domain.models import Brand, Influencer, Listing, AudienceAge, AudienceAgeSplit, AudienceGenderSplit, \
    AudienceGender, GenderEnum
from src.web.mapping import MappingRules
from src.web.views import BrandRequestDto, BrandResponseDto, InfluencerRequestDto, InfluencerResponseDto, \
    ListingResponseDto, ListingRequestDto, AudienceAgeViewDto, \
    AudienceGenderViewDto
from tests import test_mapper


def audience_split_test_factory(audience_age):
    audience_age.id = "test_id"
    audience_age.created = datetime.datetime(1, 1, 1)
    return audience_age


audience_age_data = [
    ([
         audience_split_test_factory(AudienceAge(min_age=13, max_age=17, split=0.1)),
         audience_split_test_factory(AudienceAge(min_age=18, max_age=24, split=0.1)),
         audience_split_test_factory(AudienceAge(min_age=25, max_age=34, split=0.1)),
         audience_split_test_factory(AudienceAge(min_age=35, max_age=44, split=0.1)),
         audience_split_test_factory(AudienceAge(min_age=45, max_age=54, split=0.1)),
         audience_split_test_factory(AudienceAge(min_age=55, max_age=64, split=0.1)),
         audience_split_test_factory(AudienceAge(min_age=65, split=0.1))
     ], AudienceAgeViewDto(audience_age_13_to_17_split=0.1,
                           audience_age_18_to_24_split=0.1,
                           audience_age_25_to_34_split=0.1,
                           audience_age_35_to_44_split=0.1,
                           audience_age_45_to_54_split=0.1,
                           audience_age_55_to_64_split=0.1,
                           audience_age_65_plus_split=0.1))
]

audience_gender_data = [
    (AudienceGenderSplit(audience_genders=[
        audience_split_test_factory(AudienceGender(gender=GenderEnum.MALE, split=0.1)),
        audience_split_test_factory(AudienceGender(gender=GenderEnum.FEMALE, split=0.1))
    ]), AudienceGenderViewDto(audience_male_split=0.1,
                              audience_female_split=0.1))
]


@ddt
class TestMappingRules(TestCase):

    def setUp(self) -> None:
        self.__mapper = test_mapper()
        self.__sut = MappingRules(mapper=self.__mapper)
        self.__fixture = AutoFixture()

    @data(*audience_gender_data)
    def test_map_audience_gender_to_audience_gender_request(self, data: (list[AudienceGender], AudienceGenderViewDto)):
        # arrange
        (audience_gender, expected_audience_gender_request) = data

        self.__sut.add_rules()

        audience_gender_request: AudienceGenderViewDto = self.__mapper.map(
            _from=audience_gender, to=AudienceGenderViewDto)

        # assert
        with self.subTest(msg="audience request matches"):
            self.assertEqual(audience_gender_request, expected_audience_gender_request)

    @data(*audience_gender_data)
    def test_map_audience_gender_request_to_audience_gender(self, data: (list[AudienceGender], AudienceGenderViewDto)):
        # arrange
        (audience_gender, expected_audience_gender_request) = data

        self.__sut.add_rules()

        audience_gender_split = self.__mapper.map(_from=expected_audience_gender_request, to=AudienceGenderSplit)
        expected_audience_gender_split = list(
            map(lambda x: audience_split_test_factory(x), audience_gender_split.audience_genders))

        # assert
        with self.subTest(msg="audience data matches"):
            self.assertEqual(expected_audience_gender_split, audience_gender.audience_genders)

    @data(*audience_age_data)
    def test_map_audience_age_to_audience_age_request(self, data: (list[AudienceAge], AudienceAgeViewDto)):
        # arrange
        (audience_age, expected_audience_age_request) = data

        self.__sut.add_rules()

        audience_age_request: AudienceAgeViewDto = self.__mapper.map(
            _from=AudienceAgeSplit(audience_ages=audience_age), to=AudienceAgeViewDto)

        # assert
        with self.subTest(msg="audience request matches"):
            self.assertEqual(audience_age_request, expected_audience_age_request)

    @data(*audience_age_data)
    def test_map_audience_age_request_to_audience_age(self, data: (list[AudienceAge], AudienceAgeViewDto)):
        # arrange
        (audience_age, expected_audience_age_request) = data

        self.__sut.add_rules()

        audience_age_split = self.__mapper.map(_from=expected_audience_age_request, to=AudienceAgeSplit)
        expected_audience_age_split = list(
            map(lambda x: audience_split_test_factory(x), audience_age_split.audience_ages))

        # assert
        with self.subTest(msg="audience data matches"):
            self.assertEqual(expected_audience_age_split, audience_age)

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
            self.assertEqual(influencer_response.audience_male_split, 0.0)

        # assert
        with self.subTest(msg="audience_female_splits match"):
            self.assertEqual(influencer_response.audience_female_split, 0.0)

        # assert
        with self.subTest(msg="audience_age_65_plus_splits match"):
            self.assertEqual(influencer_response.audience_age_65_plus_split, 0.0)

        # assert
        with self.subTest(msg="audience_age_55_to_64_splits match"):
            self.assertEqual(influencer_response.audience_age_55_to_64_split, 0.0)

        # assert
        with self.subTest(msg="audience_age_45_to_54_splits match"):
            self.assertEqual(influencer_response.audience_age_45_to_54_split, 0.0)

        # assert
        with self.subTest(msg="audience_age_35_to_44_splits match"):
            self.assertEqual(influencer_response.audience_age_35_to_44_split, 0.0)

        # assert
        with self.subTest(msg="audience_age_25_to_34_splits match"):
            self.assertEqual(influencer_response.audience_age_25_to_34_split, 0.0)

        # assert
        with self.subTest(msg="audience_age_18_to_24_splits match"):
            self.assertEqual(influencer_response.audience_age_18_to_24_split, 0.0)

        # assert
        with self.subTest(msg="audience_age_13_to_17_splits match"):
            self.assertEqual(influencer_response.audience_age_13_to_17_split, 0.0)

        # assert
        with self.subTest(msg="addresses match"):
            self.assertEqual(influencer_response.address, influencer.address)

    def test_map_listing_to_listing_response(self):
        # arrange
        listing = AutoFixture().create(dto=Listing, list_limit=5)

        # act
        self.__sut.add_rules()
        listing_response = self.__mapper.map(_from=listing, to=ListingResponseDto)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(listing_response.values, list(map(lambda x: x.value, listing.values)))

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(listing_response.categories,
                             list(map(lambda x: x.category, listing.categories)))

        # assert
        with self.subTest(msg="ids match"):
            self.assertEqual(listing_response.id, listing.id)

        # assert
        with self.subTest(msg="created dates match"):
            self.assertEqual(listing_response.created, listing.created)

        # assert
        with self.subTest(msg="product image match"):
            self.assertEqual(listing_response.product_image, listing.product_image)

        # assert
        with self.subTest(msg="creative guidancess match"):
            self.assertEqual(listing_response.creative_guidance, listing.creative_guidance)

        # assert
        with self.subTest(msg="product descriptions match"):
            self.assertEqual(listing_response.product_description, listing.product_description)

        # assert
        with self.subTest(msg="product titles match"):
            self.assertEqual(listing_response.product_name, listing.product_name)

        # assert
        with self.subTest(msg="listing titles match"):
            self.assertEqual(listing_response.title, listing.title)

        # assert
        with self.subTest(msg="brand auth user ids match"):
            self.assertEqual(listing_response.brand_auth_user_id, listing.brand_auth_user_id)

    def test_map_listing_response_to_listing(self):
        # arrange
        listing_response = AutoFixture().create(dto=ListingResponseDto, list_limit=5)

        # act
        self.__sut.add_rules()
        listing = self.__mapper.map(_from=listing_response, to=Listing)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(listing_response.values, list(map(lambda x: x.value, listing.values)))

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(listing_response.categories,
                             list(map(lambda x: x.category, listing.categories)))

        # assert
        with self.subTest(msg="ids match"):
            self.assertEqual(listing_response.id, listing.id)

        # assert
        with self.subTest(msg="created dates match"):
            self.assertEqual(listing_response.created, listing.created)

        # assert
        with self.subTest(msg="product image match"):
            self.assertEqual(listing_response.product_image, listing.product_image)

        # assert
        with self.subTest(msg="creative gudiancess match"):
            self.assertEqual(listing_response.creative_guidance, listing.creative_guidance)

        # assert
        with self.subTest(msg="product descriptions match"):
            self.assertEqual(listing_response.product_description, listing.product_description)

        # assert
        with self.subTest(msg="product titles match"):
            self.assertEqual(listing_response.product_name, listing.product_name)

        # assert
        with self.subTest(msg="listing titles match"):
            self.assertEqual(listing_response.title, listing.title)

        # assert
        with self.subTest(msg="brand auth user ids match"):
            self.assertEqual(listing_response.brand_auth_user_id, listing.brand_auth_user_id)

    def test_map_listing_to_listing_request(self):
        # arrange
        listing = AutoFixture().create(dto=Listing, list_limit=5)

        # act
        self.__sut.add_rules()
        listing_request = self.__mapper.map(_from=listing, to=ListingRequestDto)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(listing_request.values, list(map(lambda x: x.value, listing.values)))

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(listing_request.categories,
                             list(map(lambda x: x.category, listing.categories)))

        # assert
        with self.subTest(msg="creative gudiances match"):
            self.assertEqual(listing_request.creative_guidance, listing.creative_guidance)

        # assert
        with self.subTest(msg="product descriptions match"):
            self.assertEqual(listing_request.product_description, listing.product_description)

        # assert
        with self.subTest(msg="product titles match"):
            self.assertEqual(listing_request.product_name, listing.product_name)

        # assert
        with self.subTest(msg="listing titles match"):
            self.assertEqual(listing_request.title, listing.title)

    def test_map_listing_request_to_listing(self):
        # arrange
        listing_request = AutoFixture().create(dto=ListingRequestDto, list_limit=5)

        # act
        self.__sut.add_rules()
        listing = self.__mapper.map(_from=listing_request, to=Listing)

        # assert
        with self.subTest(msg="values match"):
            self.assertEqual(listing_request.values, list(map(lambda x: x.value, listing.values)))

        # assert
        with self.subTest(msg="categories match"):
            self.assertEqual(listing_request.categories,
                             list(map(lambda x: x.category, listing.categories)))

        # assert
        with self.subTest(msg="creative gudiances match"):
            self.assertEqual(listing_request.creative_guidance, listing.creative_guidance)

        # assert
        with self.subTest(msg="product descriptions match"):
            self.assertEqual(listing_request.product_description, listing.product_description)

        # assert
        with self.subTest(msg="product titles match"):
            self.assertEqual(listing_request.product_name, listing.product_name)

        # assert
        with self.subTest(msg="listing titles match"):
            self.assertEqual(listing_request.title, listing.title)
