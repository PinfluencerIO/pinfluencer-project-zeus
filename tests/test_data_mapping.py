from operator import itemgetter
from unittest import TestCase

from src.app import logger_factory
from src.crosscutting import AutoFixture, PinfluencerObjectMapper
from src.data.entities import create_mappings
from src.domain.models import Brand, Influencer, Listing, AudienceAge, AudienceGender, BrandListing, Collaboration, \
    CollaborationStateEnum, InfluencerListing, BrandCollaboration, InfluencerCollaboration
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

    def test_brand_collaboration_fetch_mapping(self):
        # arrange
        expected_influencer = AutoFixture().create(dto=Influencer, list_limit=5)
        expected_listing = AutoFixture().create(dto=Listing, list_limit=5)
        expected_collaboration = AutoFixture().create(dto=Collaboration, list_limit=5)
        expected_collaboration.listing_id = expected_listing.id
        expected_collaboration.influencer_auth_user_id = expected_influencer.auth_user_id

        self.__data_manager.create_fake_data([expected_collaboration, expected_listing, expected_influencer])

        # act
        brand_collaboration_from_db = self.__data_manager.session.query(BrandCollaboration).first()

        # assert
        with self.subTest(msg="collaboration ids match"):
            self.assertEqual(brand_collaboration_from_db.id, expected_collaboration.id)

        # assert
        with self.subTest(msg="influencers match"):
            self.assertEqual(brand_collaboration_from_db.influencer, expected_influencer)

        # assert
        with self.subTest(msg="listings match"):
            self.assertEqual(brand_collaboration_from_db.listing, expected_listing)

    def test_influencer_collaboration_fetch_mapping(self):
        # arrange
        expected_brand = AutoFixture().create(dto=Brand, list_limit=5)
        expected_listing = AutoFixture().create(dto=Listing, list_limit=5)
        expected_collaboration = AutoFixture().create(dto=Collaboration, list_limit=5)
        expected_collaboration.listing_id = expected_listing.id
        expected_collaboration.brand_auth_user_id = expected_brand.auth_user_id

        self.__data_manager.create_fake_data([expected_collaboration, expected_listing, expected_brand])

        # act
        brand_collaboration_from_db = self.__data_manager.session.query(InfluencerCollaboration).first()

        # assert
        with self.subTest(msg="collaboration ids match"):
            self.assertEqual(brand_collaboration_from_db.id, expected_collaboration.id)

        # assert
        with self.subTest(msg="brands match"):
            self.assertEqual(brand_collaboration_from_db.brand, expected_brand)

        # assert
        with self.subTest(msg="listings match"):
            self.assertEqual(brand_collaboration_from_db.listing, expected_listing)

    def test_influencer_listing_fetch_mapping(self):
        # arrange
        expected_brand = AutoFixture().create(dto=Brand, list_limit=5)
        listing = AutoFixture().create(dto=Listing, list_limit=5)
        listing.brand_auth_user_id = expected_brand.auth_user_id

        self.__data_manager.create_fake_data([expected_brand, listing])

        # act
        influencer_listing_in_db = self.__data_manager.session.query(InfluencerListing).first()

        # assert
        with self.subTest(msg="listing ids match"):
            self.assertEqual(listing.id, influencer_listing_in_db.id)

        # assert
        with self.subTest(msg="brands match"):
            self.assertEqual(expected_brand, influencer_listing_in_db.brand)

        # assert
        with self.subTest(msg=f"categories match"):
            self.assertCountEqual(influencer_listing_in_db.categories, listing.categories)

        # assert
        with self.subTest(msg=f"values match"):
            self.assertCountEqual(influencer_listing_in_db.values, listing.values)

    def test_brand_listing_fetch_mapping(self):
        # arrange
        listing = AutoFixture().create(dto=Listing, list_limit=5)

        collabs: list[Collaboration] = AutoFixture().create_many(dto=Collaboration, ammount=9, list_limit=5)
        for delivered_collab in collabs[0:3]:
            delivered_collab.collaboration_state = CollaborationStateEnum.DELIVERED
            delivered_collab.listing_id = listing.id

        for approved_collab in collabs[3:6]:
            approved_collab.collaboration_state = CollaborationStateEnum.APPROVED
            approved_collab.listing_id = listing.id

        for applied_collab in collabs[6:9]:
            applied_collab.collaboration_state = CollaborationStateEnum.APPLIED
            applied_collab.listing_id = listing.id

        self.__data_manager.create_fake_data([*collabs, listing])

        # act
        brand_listing_fetched_from_db = self.__data_manager.session.query(BrandListing).first()

        # assert
        with self.subTest(msg="ids match"):
            self.assertEqual(brand_listing_fetched_from_db.id, listing.id)


        with self.subTest(msg=f"delivered collabs match"):
            self.assertCountEqual(brand_listing_fetched_from_db.delivered_collaborations, collabs[0:3])

        with self.subTest(msg=f"approved collabs match"):
            self.assertCountEqual(brand_listing_fetched_from_db.approved_collaborations, collabs[3:6])

        with self.subTest(msg=f"applied collabs match"):
            self.assertCountEqual(brand_listing_fetched_from_db.applied_collaborations, collabs[6:9])

        with self.subTest(msg=f"categories match"):
            self.assertCountEqual(brand_listing_fetched_from_db.categories, listing.categories)

        with self.subTest(msg=f"values match"):
            self.assertCountEqual(brand_listing_fetched_from_db.values, listing.values)

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
            with self.subTest(msg=f"value {i} listing id is null"):
                self.assertEqual(getattr(value_from_db, 'listing_id'), None)

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
            with self.subTest(msg=f"category {i} listing id is null"):
                self.assertEqual(getattr(category_from_db, 'listing_id'), None)

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
            with self.subTest(msg=f"value {i} listing id is null"):
                self.assertEqual(getattr(value_from_db, 'listing_id'), None)

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
            with self.subTest(msg=f"category {i} listing id is null"):
                self.assertEqual(getattr(category_from_db, 'listing_id'), None)

    def test_listing_map_fetch(self):
        # arrange
        listing = AutoFixture().create(dto=Listing, list_limit=10)
        self.__data_manager.create_fake_data([listing])

        # act
        camapign_from_db = self.__data_manager.session.query(Listing).first()

        # assert
        with self.subTest(msg="listing ids match"):
            self.assertEqual(camapign_from_db.id, listing.id)

        # assert
        with self.subTest(msg="listing created dates match"):
            self.assertEqual(camapign_from_db.created, listing.created)

        # assert
        with self.subTest(msg="listing brand auth id match"):
            self.assertEqual(camapign_from_db.brand_auth_user_id, listing.brand_auth_user_id)

        # assert
        with self.subTest(msg="listing listing titles match"):
            self.assertEqual(camapign_from_db.title, listing.title)

        # assert
        with self.subTest(msg="listing product titles match"):
            self.assertEqual(camapign_from_db.product_name, listing.product_name)

        # assert
        with self.subTest(msg="listing product descriptions match"):
            self.assertEqual(camapign_from_db.product_description, listing.product_description)

        # assert
        with self.subTest(msg="listing product descriptions match"):
            self.assertEqual(camapign_from_db.creative_guidance, listing.creative_guidance)

        # assert
        with self.subTest(msg="listing listing product images match"):
            self.assertEqual(camapign_from_db.product_image, listing.product_image)

        for i in range(0, (len(listing.values) - 1)):
            expected_value = listing.values[i]
            value_from_db = camapign_from_db.values[i]

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
            with self.subTest(msg=f"value {i} listing id matches"):
                self.assertEqual(getattr(value_from_db, 'listing_id'), listing.id)

        for i in range(0, (len(listing.categories) - 1)):
            expected_category = listing.categories[i]
            category_from_db = camapign_from_db.categories[i]

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
            with self.subTest(msg=f"category {i} listing id matches"):
                self.assertEqual(getattr(category_from_db, 'listing_id'), listing.id)