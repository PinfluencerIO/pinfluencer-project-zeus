from unittest import TestCase

from src.app import logger_factory
from src.crosscutting import AutoFixture, PinfluencerObjectMapper
from src.data.entities import create_mappings
from src.domain.models import Brand, Influencer, Campaign, AudienceAge, AudienceGender
from tests import InMemorySqliteDataManager


class TestMapping(TestCase):

    def setUp(self) -> None:
        self.__data_manager = InMemorySqliteDataManager()
        create_mappings(logger=logger_factory())
        self.__mapper = PinfluencerObjectMapper(logger=logger_factory())

    def test_audience_gender_fetch_mapping(self):
        # arrange
        expected_audience_gender = AutoFixture().create(dto=AudienceGender)
        self.__data_manager.create_fake_data([expected_audience_gender])

        # act
        audience_gender_fetched_from_db = self.__data_manager.session.query(AudienceGender).first()

        # assert
        with self.subTest(msg="ids match"):
            self.assertEqual(expected_audience_gender.id, audience_gender_fetched_from_db.id)

        # assert
        with self.subTest(msg="created dates match"):
            self.assertEqual(expected_audience_gender.created, audience_gender_fetched_from_db.created)

        # assert
        with self.subTest(msg="genders match"):
            self.assertEqual(expected_audience_gender.gender, audience_gender_fetched_from_db.gender)

        # assert
        with self.subTest(msg="splits match"):
            self.assertEqual(expected_audience_gender.split, audience_gender_fetched_from_db.split)

        # assert
        with self.subTest(msg="influencer auth user ids match"):
            self.assertEqual(expected_audience_gender.influencer_auth_user_id,
                             audience_gender_fetched_from_db.influencer_auth_user_id)

    def test_audience_age_fetch_mapping(self):
        # arrange
        expected_audience_age = AutoFixture().create(dto=AudienceAge)
        self.__data_manager.create_fake_data([expected_audience_age])

        # act
        audience_age_fetched_from_db = self.__data_manager.session.query(AudienceAge).first()

        # assert
        with self.subTest(msg="ids match"):
            self.assertEqual(expected_audience_age.id, audience_age_fetched_from_db.id)

        # assert
        with self.subTest(msg="created dates match"):
            self.assertEqual(expected_audience_age.created, audience_age_fetched_from_db.created)

        # assert
        with self.subTest(msg="max ages match"):
            self.assertEqual(expected_audience_age.max_age, audience_age_fetched_from_db.max_age)

        # assert
        with self.subTest(msg="min ages match"):
            self.assertEqual(expected_audience_age.min_age, audience_age_fetched_from_db.min_age)

        # assert
        with self.subTest(msg="splits match"):
            self.assertEqual(expected_audience_age.split, audience_age_fetched_from_db.split)

        # assert
        with self.subTest(msg="influencer auth user ids match"):
            self.assertEqual(expected_audience_age.influencer_auth_user_id,
                             audience_age_fetched_from_db.influencer_auth_user_id)

    def test_brand_fetch_mapping(self):
        # arrange
        expected_brand = AutoFixture().create(dto=Brand, list_limit=10)
        self.__data_manager.create_fake_data([expected_brand])

        # act
        brand_fetched_from_db = self.__data_manager.session.query(Brand).first()

        # assert
        with self.subTest(msg="brand ids match"):
            self.assertEqual(expected_brand.id, brand_fetched_from_db.id)

        # assert
        with self.subTest(msg="brand descs match"):
            self.assertEqual(expected_brand.brand_description, brand_fetched_from_db.brand_description)

        # assert
        with self.subTest(msg="brand names match"):
            self.assertEqual(expected_brand.brand_name, brand_fetched_from_db.brand_name)

        # assert
        with self.subTest(msg="brand create dates match"):
            self.assertEqual(expected_brand.created, brand_fetched_from_db.created)

        # assert
        with self.subTest(msg="brand auth user ids match"):
            self.assertEqual(expected_brand.auth_user_id, brand_fetched_from_db.auth_user_id)

        # assert
        with self.subTest(msg="brand insta handles match"):
            self.assertEqual(expected_brand.insta_handle, brand_fetched_from_db.insta_handle)

        # assert
        with self.subTest(msg="brand websites match"):
            self.assertEqual(expected_brand.website, brand_fetched_from_db.website)

        # assert
        with self.subTest(msg="brand header images match"):
            self.assertEqual(expected_brand.header_image, brand_fetched_from_db.header_image)

        # assert
        with self.subTest(msg="brand logos match"):
            self.assertEqual(expected_brand.logo, brand_fetched_from_db.logo)

        for i in range(0, (len(expected_brand.values) - 1)):
            expected_value = expected_brand.values[i]
            value_from_db = brand_fetched_from_db.values[i]

            # assert
            with self.subTest(msg=f"value {i} ids match"):
                self.assertEqual(value_from_db.id, expected_value.id)

            # assert
            with self.subTest(msg=f"value {i} values match"):
                self.assertEqual(value_from_db.value, expected_value.value)

            # assert
            with self.subTest(msg=f"value {i} created dates match"):
                self.assertEqual(value_from_db.created, expected_value.created)

            # assert
            with self.subTest(msg=f"value {i} brand ids match"):
                self.assertEqual(getattr(value_from_db, 'brand_id'), expected_brand.auth_user_id)

            # assert
            with self.subTest(msg=f"value {i} influencer id is null"):
                self.assertEqual(getattr(value_from_db, 'influencer_id'), None)

            # assert
            with self.subTest(msg=f"value {i} campaign id is null"):
                self.assertEqual(getattr(value_from_db, 'campaign_id'), None)

        for i in range(0, (len(expected_brand.categories) - 1)):
            expected_category = expected_brand.categories[i]
            category_from_db = brand_fetched_from_db.categories[i]

            # assert
            with self.subTest(msg=f"category {i} ids match"):
                self.assertEqual(category_from_db.id, expected_category.id)

            # assert
            with self.subTest(msg=f"category {i} categories match"):
                self.assertEqual(category_from_db.category, expected_category.category)

            # assert
            with self.subTest(msg=f"category {i} created dates match"):
                self.assertEqual(category_from_db.created, expected_category.created)

            # assert
            with self.subTest(msg=f"category {i} brand ids match"):
                self.assertEqual(getattr(category_from_db, 'brand_id'), expected_brand.auth_user_id)

            # assert
            with self.subTest(msg=f"category {i} influencer id is null"):
                self.assertEqual(getattr(category_from_db, 'influencer_id'), None)

            # assert
            with self.subTest(msg=f"category {i} campaign id is null"):
                self.assertEqual(getattr(category_from_db, 'campaign_id'), None)

    def test_influencer_fetch_mapping(self):
        # arrange
        influencer = AutoFixture().create(dto=Influencer, list_limit=10)
        self.__data_manager.create_fake_data([influencer])

        # act
        influencer_in_db = self.__data_manager.session.query(Influencer).first()

        # assert
        with self.subTest(msg="influencer ids match"):
            self.assertEqual(influencer_in_db.id, influencer.id)

        # assert
        with self.subTest(msg="influencer auth user ids match"):
            self.assertEqual(influencer_in_db.auth_user_id, influencer.auth_user_id)

        # assert
        with self.subTest(msg="influencer created dates match"):
            self.assertEqual(influencer_in_db.created, influencer.created)

        # assert
        with self.subTest(msg="influencer websites match"):
            self.assertEqual(influencer_in_db.website, influencer.website)

        # assert
        with self.subTest(msg="influencer insta_handles match"):
            self.assertEqual(influencer_in_db.insta_handle, influencer.insta_handle)

        # assert
        with self.subTest(msg="influencer addresses match"):
            self.assertEqual(influencer_in_db.address, influencer.address)

        # assert
        with self.subTest(msg="influencer audience_age_13_to_17_split match"):
            self.assertEqual(influencer_in_db.audience_age_13_to_17_split, influencer.audience_age_13_to_17_split)

        # assert
        with self.subTest(msg="influencer audience_age_18_to_24_split match"):
            self.assertEqual(influencer_in_db.audience_age_18_to_24_split, influencer.audience_age_18_to_24_split)

        # assert
        with self.subTest(msg="influencer audience_age_25_to_34_split match"):
            self.assertEqual(influencer_in_db.audience_age_25_to_34_split, influencer.audience_age_25_to_34_split)

        # assert
        with self.subTest(msg="influencer audience_age_35_to_44_split match"):
            self.assertEqual(influencer_in_db.audience_age_35_to_44_split, influencer.audience_age_35_to_44_split)

        # assert
        with self.subTest(msg="influencer audience_age_45_to_54_split match"):
            self.assertEqual(influencer_in_db.audience_age_45_to_54_split, influencer.audience_age_45_to_54_split)

        # assert
        with self.subTest(msg="influencer audience_age_45_to_54_split match"):
            self.assertEqual(influencer_in_db.audience_age_55_to_64_split, influencer.audience_age_55_to_64_split)

        # assert
        with self.subTest(msg="influencer audience_age_65_plus_split match"):
            self.assertEqual(influencer_in_db.audience_age_65_plus_split, influencer.audience_age_65_plus_split)

        # assert
        with self.subTest(msg="influencer audience_female_split match"):
            self.assertEqual(influencer_in_db.audience_female_split, influencer.audience_female_split)

        # assert
        with self.subTest(msg="influencer audience_male_split match"):
            self.assertEqual(influencer_in_db.audience_male_split, influencer.audience_male_split)

        # assert
        with self.subTest(msg="influencer bio match"):
            self.assertEqual(influencer_in_db.bio, influencer.bio)

        # assert
        with self.subTest(msg="influencer image match"):
            self.assertEqual(influencer_in_db.image, influencer.image)

        for i in range(0, (len(influencer.values) - 1)):
            expected_value = influencer.values[i]
            value_from_db = influencer_in_db.values[i]

            # assert
            with self.subTest(msg=f"value {i} ids match"):
                self.assertEqual(value_from_db.id, expected_value.id)

            # assert
            with self.subTest(msg=f"value {i} values match"):
                self.assertEqual(value_from_db.value, expected_value.value)

            # assert
            with self.subTest(msg=f"value {i} created dates match"):
                self.assertEqual(value_from_db.created, expected_value.created)

            # assert
            with self.subTest(msg=f"value {i} brand ids match"):
                self.assertEqual(getattr(value_from_db, 'brand_id'), None)

            # assert
            with self.subTest(msg=f"value {i} influencer id is null"):
                self.assertEqual(getattr(value_from_db, 'influencer_id'), influencer.auth_user_id)

            # assert
            with self.subTest(msg=f"value {i} campaign id is null"):
                self.assertEqual(getattr(value_from_db, 'campaign_id'), None)

        for i in range(0, (len(influencer.categories) - 1)):
            expected_category = influencer.categories[i]
            category_from_db = influencer_in_db.categories[i]

            # assert
            with self.subTest(msg=f"category {i} ids match"):
                self.assertEqual(category_from_db.id, expected_category.id)

            # assert
            with self.subTest(msg=f"category {i} categories match"):
                self.assertEqual(category_from_db.category, expected_category.category)

            # assert
            with self.subTest(msg=f"category {i} created dates match"):
                self.assertEqual(category_from_db.created, expected_category.created)

            # assert
            with self.subTest(msg=f"category {i} brand ids match"):
                self.assertEqual(getattr(category_from_db, 'brand_id'), None)

            # assert
            with self.subTest(msg=f"category {i} influencer id matches"):
                self.assertEqual(getattr(category_from_db, 'influencer_id'), influencer.auth_user_id)

            # assert
            with self.subTest(msg=f"category {i} campaign id is null"):
                self.assertEqual(getattr(category_from_db, 'campaign_id'), None)

    def test_campaign_map_fetch(self):
        # arrange
        campaign = AutoFixture().create(dto=Campaign, list_limit=10)
        self.__data_manager.create_fake_data([campaign])

        # act
        camapign_from_db = self.__data_manager.session.query(Campaign).first()

        # assert
        with self.subTest(msg="campaign ids match"):
            self.assertEqual(camapign_from_db.id, campaign.id)

        # assert
        with self.subTest(msg="campaign created dates match"):
            self.assertEqual(camapign_from_db.created, campaign.created)

        # assert
        with self.subTest(msg="campaign brand auth id match"):
            self.assertEqual(camapign_from_db.brand_auth_user_id, campaign.brand_auth_user_id)

        # assert
        with self.subTest(msg="campaign campaign titles match"):
            self.assertEqual(camapign_from_db.campaign_title, campaign.campaign_title)

        # assert
        with self.subTest(msg="campaign success descriptions match"):
            self.assertEqual(camapign_from_db.success_description, campaign.success_description)

        # assert
        with self.subTest(msg="campaign product titles match"):
            self.assertEqual(camapign_from_db.product_title, campaign.product_title)

        # assert
        with self.subTest(msg="campaign product descriptions match"):
            self.assertEqual(camapign_from_db.product_description, campaign.product_description)

        # assert
        with self.subTest(msg="campaign product descriptions match"):
            self.assertEqual(camapign_from_db.objective, campaign.objective)

        # assert
        with self.subTest(msg="campaign campaign discount codes match"):
            self.assertEqual(camapign_from_db.campaign_discount_code, campaign.campaign_discount_code)

        # assert
        with self.subTest(msg="campaign campaign states match"):
            self.assertEqual(camapign_from_db.campaign_state, campaign.campaign_state)

        # assert
        with self.subTest(msg="campaign campaign hashtags match"):
            self.assertEqual(camapign_from_db.campaign_hashtag, campaign.campaign_hashtag)

        # assert
        with self.subTest(msg="campaign campaign hashtags match"):
            self.assertEqual(camapign_from_db.campaign_product_link, campaign.campaign_product_link)

        # assert
        with self.subTest(msg="campaign campaign product images match"):
            self.assertEqual(camapign_from_db.product_image, campaign.product_image)

        for i in range(0, (len(campaign.campaign_values) - 1)):
            expected_value = campaign.campaign_values[i]
            value_from_db = camapign_from_db.campaign_values[i]

            # assert
            with self.subTest(msg=f"value {i} ids match"):
                self.assertEqual(value_from_db.id, expected_value.id)

            # assert
            with self.subTest(msg=f"value {i} values match"):
                self.assertEqual(value_from_db.value, expected_value.value)

            # assert
            with self.subTest(msg=f"value {i} created dates match"):
                self.assertEqual(value_from_db.created, expected_value.created)

            # assert
            with self.subTest(msg=f"value {i} brand id is null"):
                self.assertEqual(getattr(value_from_db, 'brand_id'), None)

            # assert
            with self.subTest(msg=f"value {i} influencer id is null"):
                self.assertEqual(getattr(value_from_db, 'influencer_id'), None)

            # assert
            with self.subTest(msg=f"value {i} campaign id matches"):
                self.assertEqual(getattr(value_from_db, 'campaign_id'), campaign.id)

        for i in range(0, (len(campaign.campaign_categories) - 1)):
            expected_category = campaign.campaign_categories[i]
            category_from_db = camapign_from_db.campaign_categories[i]

            # assert
            with self.subTest(msg=f"category {i} ids match"):
                self.assertEqual(category_from_db.id, expected_category.id)

            # assert
            with self.subTest(msg=f"category {i} categories match"):
                self.assertEqual(category_from_db.category, expected_category.category)

            # assert
            with self.subTest(msg=f"category {i} created dates match"):
                self.assertEqual(category_from_db.created, expected_category.created)

            # assert
            with self.subTest(msg=f"category {i} brand ids match"):
                self.assertEqual(getattr(category_from_db, 'brand_id'), None)

            # assert
            with self.subTest(msg=f"category {i} influencer id is null"):
                self.assertEqual(getattr(category_from_db, 'influencer_id'), None)

            # assert
            with self.subTest(msg=f"category {i} campaign id matches"):
                self.assertEqual(getattr(category_from_db, 'campaign_id'), campaign.id)