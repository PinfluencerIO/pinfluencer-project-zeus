from unittest import TestCase
from unittest.mock import Mock, MagicMock

from callee import Captor

from src._types import ImageRepository
from src.app import logger_factory
from src.crosscutting import AutoFixture
from src.data.repositories import SqlAlchemyBrandRepository, SqlAlchemyInfluencerRepository, CognitoAuthUserRepository, \
    CognitoAuthService, SqlAlchemyListingRepository, SqlAlchemyNotificationRepository, SqlAlchemyAudienceAgeRepository, \
    SqlAlchemyAudienceGenderRepository, SqlAlchemyBrandListingRepository, SqlAlchemyCollaborationRepository
from src.domain.models import Brand, Influencer, User, Listing, Notification, AudienceAgeSplit, AudienceAge, \
    AudienceGenderSplit, AudienceGender, BrandListing, Collaboration, CollaborationStateEnum
from src.exceptions import AlreadyExistsException, NotFoundException
from tests import InMemorySqliteDataManager


class BrandRepositoryTestCase(TestCase):

    def setUp(self):
        self._data_manager = InMemorySqliteDataManager()
        self._image_repository: ImageRepository = Mock()
        self._sut = SqlAlchemyBrandRepository(data_manager=self._data_manager,
                                              image_repository=self._image_repository,
                                              logger=Mock())


class TestBaseRepository(BrandRepositoryTestCase):

    def test_commit(self):
        # arrange
        expected_brand = AutoFixture().create(dto=Brand,
                                              list_limit=5)
        expected_brand_id = expected_brand.id
        brand_names = [expected_brand.brand_name, "new_brand_name"]
        self._data_manager.create_fake_data([expected_brand])

        # act
        self._data_manager \
            .session \
            .query(Brand) \
            .filter(Brand.id == expected_brand.id) \
            .first().brand_name = brand_names[1]
        self._sut.save()
        self._data_manager.session.close()

        # assert
        with self.subTest(msg="brand name has been changed in db"):
            assert self._data_manager \
                       .session \
                       .query(Brand) \
                       .filter(Brand.id == expected_brand_id) \
                       .first().brand_name == brand_names[1]

    def test_commit_when_data_not_committed(self):
        # arrange
        expected_brand = AutoFixture().create(dto=Brand,
                                              list_limit=5)
        expected_brand_id = expected_brand.id
        brand_names = [expected_brand.brand_name, "new_brand_name"]
        self._data_manager.create_fake_data([expected_brand])

        # act
        self._data_manager \
            .session \
            .query(Brand) \
            .filter(Brand.id == expected_brand.id) \
            .first().brand_name = brand_names[1]
        self._data_manager.session.close()

        # assert
        with self.subTest(msg="brand name has been changed in db"):
            assert self._data_manager \
                       .session \
                       .query(Brand) \
                       .filter(Brand.id == expected_brand_id) \
                       .first().brand_name == brand_names[0]

    def test_load_by_id(self):
        # arrange
        expected_brand = AutoFixture().create(dto=Brand, list_limit=5)
        self._data_manager.create_fake_data([expected_brand])

        # act
        actual_brand = self._sut.load_by_id(id_=expected_brand.id)

        # assert
        with self.subTest(msg="brands match"):
            self.assertEqual(expected_brand, actual_brand)

    def test_load_by_id_when_brand_cannot_be_found(self):
        self.assertRaises(NotFoundException, lambda: self._sut.load_by_id(id_="1234"))

    def test_load_collection(self):
        # arrange
        expected_brands = AutoFixture().create_many(dto=Brand, list_limit=5, ammount=10)
        self._data_manager.create_fake_data(expected_brands)

        # act
        actual_brands = self._sut.load_collection()

        # assert
        with self.subTest(msg="brands match"):
            assert expected_brands == actual_brands

    def test_load_collection_when_no_brands_exist(self):
        # arrange/act
        actual_brands = self._sut.load_collection()

        # assert
        assert [] == actual_brands


class TestUserRepository(BrandRepositoryTestCase):

    def test_load_for_auth_user(self):
        # arrange
        expected = AutoFixture().create(dto=Brand, list_limit=5)
        self._data_manager.create_fake_data([expected])

        # act
        actual = self._sut.load_for_auth_user(auth_user_id=expected.auth_user_id)

        # assert
        with self.subTest(msg="brands match"):
            assert actual == expected

    def test_load_for_auth_user_when_brand_not_found(self):
        self.assertRaises(NotFoundException, lambda: self._sut.load_for_auth_user(auth_user_id="12341"))

    def test_write_new_for_auth_user(self):
        # arrange
        expected = AutoFixture().create(dto=Brand, list_limit=5)

        # act
        returned_user = self._sut.write_new_for_auth_user(auth_user_id=expected.auth_user_id,
                                                          payload=expected)
        actual = self._sut.load_by_id(id_=expected.id)

        # assert
        with self.subTest(msg="brand in db matches returned brand, which also matches brand loaded by id"):
            assert expected == returned_user == actual

    def test_write_new_for_auth_user_when_already_exists(self):
        # arrange
        expected = AutoFixture().create(dto=Brand, list_limit=5)
        brand_to_create = AutoFixture().create(dto=Brand, list_limit=5)
        brand_to_create.auth_user_id = expected.auth_user_id
        self._data_manager.create_fake_data([expected])

        # act/assert
        with self.subTest(msg="repo raises an error"):
            self.assertRaises(AlreadyExistsException,
                              lambda: self._sut.write_new_for_auth_user(auth_user_id=expected.auth_user_id,
                                                                        payload=brand_to_create))
        actual = self._sut.load_for_auth_user(auth_user_id=brand_to_create.auth_user_id)

        # assert
        with self.subTest(msg="brands do not match"):
            assert actual != brand_to_create

        # assert
        with self.subTest(msg="brand does not change"):
            assert actual == expected


class TestBrandRepository(BrandRepositoryTestCase):

    def test_write_new_for_auth_user(self):
        # arrange
        expected = AutoFixture().create(dto=Brand, list_limit=5)

        # act
        self._sut.write_new_for_auth_user(auth_user_id=expected.auth_user_id,
                                          payload=expected)
        actual = self._sut.load_by_id(id_=expected.id)

        # assert
        with self.subTest(msg="brand is retrieved"):
            self.assertEqual(actual, expected)


class TestInfluencerRepository(TestCase):

    def setUp(self):
        self.__data_manager = InMemorySqliteDataManager()
        self.__image_repository = Mock()
        self.__sut = SqlAlchemyInfluencerRepository(data_manager=self.__data_manager,
                                                    image_repository=self.__image_repository,
                                                    logger=Mock())

    def test_write_new_for_auth_user(self):
        # arrange
        expected = AutoFixture().create(dto=Influencer, list_limit=5)

        # act
        returned_influencer = self.__sut.write_new_for_auth_user(auth_user_id=expected.auth_user_id,
                                                                 payload=expected)
        actual = self.__sut.load_by_id(id_=expected.id)

        # assert
        assert actual == expected == returned_influencer


class TestAuthUserRepository(TestCase):

    def setUp(self) -> None:
        self.__auth_user_service: CognitoAuthService = Mock()
        self.__sut = CognitoAuthUserRepository(self.__auth_user_service,
                                               logger=Mock())

    def test_update_brand_claims(self):
        # arrange
        expected_user: User = AutoFixture().create(dto=User, list_limit=5)
        self.__sut._update_user_claims = MagicMock()

        # act
        self.__sut.update_brand_claims(user=expected_user, auth_user_id="1234")

        # assert
        self.__sut._update_user_claims.assert_called_once_with(user=expected_user, type='brand',
                                                               auth_user_id="1234")

    def test_update_influencer_claims(self):
        # arrange
        payload_captor = Captor()
        expected_influencer: User = AutoFixture().create(dto=User, list_limit=5)
        self.__auth_user_service.update_user_claims = MagicMock()

        # act
        self.__sut.update_influencer_claims(user=expected_influencer, auth_user_id="1234")

        # assert
        with self.subTest(msg="auth repo was called"):
            self.__auth_user_service.update_user_claims.assert_called_once_with(
                username="1234",
                attributes=payload_captor)
        expected_attributes = [
            {
                "Name": "family_name",
                "Value": expected_influencer.family_name
            },
            {
                "Name": "given_name",
                "Value": expected_influencer.given_name
            },
            {
                "Name": "email",
                "Value": expected_influencer.email
            },
            {
                "Name": "custom:usertype",
                "Value": "influencer"
            }
        ]
        actual_attributes = payload_captor.arg
        actual_attributes = sorted(actual_attributes, key=lambda d: d['Name'])
        expected_attributes = sorted(expected_attributes, key=lambda d: d['Name'])

        # assert
        with self.subTest(msg="attributes match"):
            self.assertListEqual(expected_attributes, actual_attributes)

    def test_update_influencer_claims_when_attributes_are_missing(self):
        # arrange
        payload_captor = Captor()
        expected_influencer: User = AutoFixture().create(dto=User, list_limit=5)
        expected_influencer.family_name = None
        expected_influencer.email = None
        self.__auth_user_service.update_user_claims = MagicMock()

        # act
        self.__sut.update_influencer_claims(user=expected_influencer, auth_user_id="1234")

        # assert
        with self.subTest(msg="auth repo was called"):
            self.__auth_user_service.update_user_claims.assert_called_once_with(
                username="1234",
                attributes=payload_captor)
        expected_attributes = [
            {
                "Name": "given_name",
                "Value": expected_influencer.given_name
            },
            {
                "Name": "custom:usertype",
                "Value": "influencer"
            }
        ]
        actual_attributes = payload_captor.arg
        actual_attributes = sorted(actual_attributes, key=lambda d: d['Name'])
        expected_attributes = sorted(expected_attributes, key=lambda d: d['Name'])

        # assert
        with self.subTest(msg="attributes match"):
            self.assertListEqual(expected_attributes, actual_attributes)

    def test_get_user_by_id(self):
        # arrange
        expected_brand = AutoFixture().create(dto=User, list_limit=5)
        self.__auth_user_service.get_user = MagicMock(return_value={
            'Username': "1234",
            'UserAttributes': [
                {
                    'Name': 'given_name',
                    'Value': expected_brand.given_name
                },
                {
                    'Name': 'family_name',
                    'Value': expected_brand.family_name
                },
                {
                    'Name': 'email',
                    'Value': expected_brand.email
                }
            ]
        })

        # act
        actual_brand = self.__sut.get_by_id(_id="1234")

        # assert
        with self.subTest(msg="first name matches"):
            assert actual_brand.given_name == expected_brand.given_name

        # assert
        with self.subTest(msg="last name matches"):
            assert actual_brand.family_name == expected_brand.family_name

        # assert
        with self.subTest(msg="email matches"):
            assert actual_brand.email == expected_brand.email


class TestBrandListingRepository(TestCase):

    def setUp(self) -> None:
        self.__data_manager = InMemorySqliteDataManager()
        self.__sut = SqlAlchemyBrandListingRepository(data_manager=self.__data_manager,
                                                      logger=Mock())

    def test_load_for_auth_brand(self):
        # arrange
        brand_listings = AutoFixture().create_many(dto=BrandListing, ammount=5, list_limit=5)
        self.__sut._load_for_auth_owner = MagicMock(return_value=brand_listings)

        # act
        returned_listings = self.__sut.load_for_auth_brand(auth_user_id="1234")

        # assert
        with self.subTest(msg="repo was called"):
            self.__sut._load_for_auth_owner.assert_called_once_with(auth_user_id="1234",
                                                                    model_entity_field=BrandListing.brand_auth_user_id,
                                                                    model=BrandListing)

        # assert
        with self.subTest(msg="listings were returned"):
            self.assertCountEqual(returned_listings, brand_listings)


class TestListingRepository(TestCase):

    def setUp(self) -> None:
        self.__data_manager = InMemorySqliteDataManager()
        self.__image_repository: ImageRepository = Mock()
        self.__sut = SqlAlchemyListingRepository(data_manager=self.__data_manager,
                                                 image_repository=self.__image_repository,
                                                 logger=Mock())

    def test_write_for_new_brand(self):
        # arrange
        brand_in_db = AutoFixture().create(dto=Brand, list_limit=5)
        listing_payload: Listing = AutoFixture().create(dto=Listing, list_limit=5)

        # act
        self.__data_manager.create_fake_data(objects=[brand_in_db])
        returned_listing: Listing = self.__sut.write_new_for_brand(payload=listing_payload,
                                                                   auth_user_id=brand_in_db.auth_user_id)

        listing_loaded_from_db: Listing = self.__sut.load_by_id(id_=listing_payload.id)

        # assert
        with self.subTest(msg="brand ids match"):
            assert returned_listing.brand_auth_user_id == listing_loaded_from_db.brand_auth_user_id == brand_in_db.auth_user_id

        # assert
        with self.subTest(msg="listing fields match"):
            assert listing_payload == listing_loaded_from_db == returned_listing

    def test_get_by_id(self):
        # arrange
        listing = AutoFixture().create(dto=Listing, list_limit=5)
        self.__data_manager.create_fake_data([listing])

        # act
        listing_returned = self.__sut.load_by_id(id_=listing.id)

        # assert
        assert listing_returned == listing

    def test_load_for_brand(self):
        # arrange
        brand = AutoFixture().create(dto=Brand, list_limit=5)
        listings = AutoFixture().create_many(dto=Listing, list_limit=5, ammount=10)
        for listing in listings:
            listing.brand_auth_user_id = brand.auth_user_id
        self.__data_manager.create_fake_data([brand])
        self.__data_manager.create_fake_data(listings)

        # act
        returned_listings = self.__sut.load_for_auth_brand(auth_user_id=brand.auth_user_id)

        # assert
        self.assertEquals(listings, returned_listings)


class TestCollaborationRepository(TestCase):

    def setUp(self) -> None:
        self.__data_manager = InMemorySqliteDataManager()
        self.__sut = SqlAlchemyCollaborationRepository(data_manager=self.__data_manager,
                                                       logger=Mock())

    def test_create_for_influencer(self):
        # arrange
        collaboration = AutoFixture().create(dto=Collaboration, list_limit=5)
        collaboration.influencer_auth_user_id = ""
        collaboration.collaboration_state = None
        self.__sut._write_new_for_owner = MagicMock()

        # act
        self.__sut.write_new_for_influencer(payload=collaboration,
                                            auth_user_id="1234")

        captor = Captor()

        # assert
        with self.subTest(msg="repo was called"):
            self.__sut._write_new_for_owner.assert_called_once_with(payload=collaboration,
                                                                    foreign_key_setter=captor)
        # assert
        with self.subTest(msg="field setter set auth user id"):
            captor.arg(collaboration)
            self.assertEqual("1234", collaboration.influencer_auth_user_id)

        # assert
        with self.subTest(msg="field setter set collab state"):
            self.assertEqual(CollaborationStateEnum.APPLIED, collaboration.collaboration_state)


class TestNotificationRepository(TestCase):

    def setUp(self) -> None:
        self.__data_manager = InMemorySqliteDataManager()
        self.__sut = SqlAlchemyNotificationRepository(data_manager=self.__data_manager,
                                                      logger=logger_factory())

    def test_write_for_auth_user(self):
        # arrange
        notification = AutoFixture().create(dto=Notification)
        notification.read = True
        notification.sender_auth_user_id = None

        # act
        returned_notification = self.__sut.write_new_for_auth_user(auth_user_id="1234", payload=notification)

        # assert
        with self.subTest(msg="notification matches notification in db"):
            notification_in_db = self.__sut.load_by_id(id_=notification.id)
            assert notification == notification_in_db == returned_notification


class TestAudienceGenderRepository(TestCase):

    def setUp(self) -> None:
        self.__data_manager = InMemorySqliteDataManager()
        self.__sut = SqlAlchemyAudienceGenderRepository(data_manager=self.__data_manager,
                                                        logger=logger_factory())

    def test_write_for_influencer(self):
        # arrange
        audience_gender_split = AutoFixture().create(dto=AudienceGenderSplit, list_limit=15)
        self.__sut._write_new_for_owner = MagicMock(return_value=audience_gender_split)

        # act
        returned_audience_gender_split = \
            self.__sut.write_new_for_influencer(payload=audience_gender_split,
                                                auth_user_id="user1234")

        # assert
        for audience_gender in audience_gender_split.audience_genders:
            captor = Captor()
            with self.subTest(msg=f"base repo was called for gender"
                                  f"{audience_gender.gender}"):
                self.__sut._write_new_for_owner.assert_any_call(payload=audience_gender,
                                                                foreign_key_setter=captor)

            with self.subTest(msg=f"field setter sets correct field for gender"
                                  f"{audience_gender.gender}"):
                captor.arg(audience_gender)
                self.assertEqual(audience_gender.influencer_auth_user_id, "user1234")

            with self.subTest(msg="captured repo value was returned for gender"
                                  f"{audience_gender.gender}"):
                self.assertEqual(returned_audience_gender_split, audience_gender_split)

    def test_load_for_influencer(self):
        # arrange
        audience_genders = AutoFixture().create_many(dto=AudienceGender, ammount=5)
        self.__sut._load_for_auth_owner = MagicMock(return_value=audience_genders)

        # act
        returned_audience_gender_split = self.__sut.load_for_influencer(auth_user_id="user1234")

        # assert
        with self.subTest(msg=f"base repo was called"):
            self.__sut._load_for_auth_owner.assert_called_once_with(auth_user_id="user1234",
                                                                    model=AudienceGender,
                                                                    model_entity_field=AudienceGender.influencer_auth_user_id)

        with self.subTest(msg="captured repo value was returned gender ranges"):
            self.assertEqual(returned_audience_gender_split, AudienceGenderSplit(audience_genders=audience_genders))


class TestAudienceAgeRepository(TestCase):

    def setUp(self) -> None:
        self.__data_manager = InMemorySqliteDataManager()
        self.__sut = SqlAlchemyAudienceAgeRepository(data_manager=self.__data_manager,
                                                     logger=logger_factory())

    def test_write_for_influencer(self):
        # arrange
        audience_age_split = AutoFixture().create(dto=AudienceAgeSplit, list_limit=15)
        self.__sut._write_new_for_owner = MagicMock(return_value=audience_age_split)

        # act
        returned_audience_age_split = \
            self.__sut.write_new_for_influencer(payload=audience_age_split,
                                                auth_user_id="user1234")

        # assert
        for audience_age in audience_age_split.audience_ages:
            captor = Captor()
            with self.subTest(msg=f"base repo was called for age ranges"
                                  f"{audience_age.min_age}-{audience_age.max_age}"):
                self.__sut._write_new_for_owner.assert_any_call(payload=audience_age,
                                                                foreign_key_setter=captor)

            with self.subTest(msg=f"field setter sets correct field for age ranges"
                                  f"{audience_age.min_age}-{audience_age.max_age}"):
                captor.arg(audience_age)
                self.assertEqual(audience_age.influencer_auth_user_id, "user1234")

            with self.subTest(msg="captured repo value was returned age ranges"
                                  f"{audience_age.min_age}-{audience_age.max_age}"):
                self.assertEqual(returned_audience_age_split, audience_age_split)

    def test_load_for_influencer(self):
        # arrange
        audience_ages = AutoFixture().create_many(dto=AudienceAge, ammount=5)
        self.__sut._load_for_auth_owner = MagicMock(return_value=audience_ages)

        # act
        returned_audience_age_split = self.__sut.load_for_influencer(auth_user_id="user1234")

        # assert
        with self.subTest(msg=f"base repo was called"):
            self.__sut._load_for_auth_owner.assert_called_once_with(auth_user_id="user1234",
                                                                    model=AudienceAge,
                                                                    model_entity_field=AudienceAge.influencer_auth_user_id)

        with self.subTest(msg="captured repo value was returned age ranges"):
            self.assertEqual(returned_audience_age_split, AudienceAgeSplit(audience_ages=audience_ages))
