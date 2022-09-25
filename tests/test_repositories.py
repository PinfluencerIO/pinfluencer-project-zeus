from unittest import TestCase
from unittest.mock import Mock, MagicMock

from callee import Captor

from src._types import ImageRepository
from src.crosscutting import AutoFixture
from src.data.repositories import SqlAlchemyBrandRepository, SqlAlchemyInfluencerRepository, CognitoAuthUserRepository, \
    CognitoAuthService, SqlAlchemyCampaignRepository
from src.domain.models import Brand, Influencer, User, Campaign
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
                       .filter(Brand.id == expected_brand.id) \
                       .first().brand_name == brand_names[1]

    def test_load_by_id(self):
        # arrange
        expected_brand = AutoFixture().create(dto=Brand, list_limit=5)
        self._data_manager.create_fake_data([expected_brand])

        # act
        actual_brand = self._sut.load_by_id(id_=expected_brand.id)

        # assert
        with self.subTest(msg="brands match"):
            assert expected_brand == actual_brand

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
        assert actual == expected


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
        payload_captor = Captor()
        expected_user = AutoFixture().create(dto=User, list_limit=5)
        self.__auth_user_service.update_user_claims = MagicMock()

        # act
        self.__sut.update_brand_claims(user=expected_user)

        # assert
        with self.subTest(msg="auth service was called"):
            self.__auth_user_service.update_user_claims.assert_called_once_with(username=expected_user.auth_user_id,
                                                                                attributes=payload_captor)
        expected_attributes = [
            {
                "Name": "family_name",
                "Value": expected_user.last_name
            },
            {
                "Name": "given_name",
                "Value": expected_user.first_name
            },
            {
                "Name": "email",
                "Value": expected_user.email
            },
            {
                "Name": "custom:usertype",
                "Value": "brand"
            }
        ]
        actual_attributes = payload_captor.arg
        actual_attributes = sorted(actual_attributes, key=lambda d: d['Name'])
        expected_attributes = sorted(expected_attributes, key=lambda d: d['Name'])

        # assert
        with self.subTest(msg="attributes match"):
            self.assertListEqual(expected_attributes, actual_attributes)

    def test_update_influencer_claims(self):
        # arrange
        payload_captor = Captor()
        expected_influencer = AutoFixture().create(dto=User, list_limit=5)
        self.__auth_user_service.update_user_claims = MagicMock()

        # act
        self.__sut.update_influencer_claims(user=expected_influencer)

        # assert
        with self.subTest(msg="auth repo was called"):
            self.__auth_user_service.update_user_claims.assert_called_once_with(
                username=expected_influencer.auth_user_id,
                attributes=payload_captor)
        expected_attributes = [
            {
                "Name": "family_name",
                "Value": expected_influencer.last_name
            },
            {
                "Name": "given_name",
                "Value": expected_influencer.first_name
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

    def test_get_user_by_id(self):
        # arrange
        expected_brand = AutoFixture().create(dto=User, list_limit=5)
        self.__auth_user_service.get_user = MagicMock(return_value={
            'Username': expected_brand.auth_user_id,
            'UserAttributes': [
                {
                    'Name': 'given_name',
                    'Value': expected_brand.first_name
                },
                {
                    'Name': 'family_name',
                    'Value': expected_brand.last_name
                },
                {
                    'Name': 'email',
                    'Value': expected_brand.email
                }
            ]
        })

        # act
        actual_brand = self.__sut.get_by_id(_id=expected_brand.auth_user_id)

        # assert
        with self.subTest(msg="first name matches"):
            assert actual_brand.first_name == expected_brand.first_name

        # assert
        with self.subTest(msg="last name matches"):
            assert actual_brand.last_name == expected_brand.last_name

        # assert
        with self.subTest(msg="email matches"):
            assert actual_brand.email == expected_brand.email


class TestCampaignRepository(TestCase):

    def setUp(self) -> None:
        self.__data_manager = InMemorySqliteDataManager()
        self.__image_repository: ImageRepository = Mock()
        self.__sut = SqlAlchemyCampaignRepository(data_manager=self.__data_manager,
                                                  image_repository=self.__image_repository,
                                                  logger=Mock())

    def test_write_for_new_brand(self):
        # arrange
        brand_in_db = AutoFixture().create(dto=Brand, list_limit=5)
        campaign_payload: Campaign = AutoFixture().create(dto=Campaign, list_limit=5)

        # act
        self.__data_manager.create_fake_data(objects=[brand_in_db])
        returned_campaign: Campaign = self.__sut.write_new_for_brand(payload=campaign_payload,
                                                                     auth_user_id=brand_in_db.auth_user_id)

        campaign_loaded_from_db: Campaign = self.__sut.load_by_id(id_=campaign_payload.id)

        # assert
        with self.subTest(msg="brand ids match"):
            assert returned_campaign.brand_id == campaign_loaded_from_db.brand_id == brand_in_db.id

        # assert
        with self.subTest(msg="campaign fields match"):
            assert campaign_payload == campaign_loaded_from_db == returned_campaign

    def test_write_for_new_brand_when_brand_does_not_exist(self):
        # arrange
        campaign = AutoFixture().create(dto=Campaign, list_limit=5)

        # act/assert
        self.assertRaises(NotFoundException, lambda: self.__sut
                          .write_new_for_brand(payload=campaign,
                                               auth_user_id="1234"))

    def test_get_by_id(self):
        # arrange
        campaign = AutoFixture().create(dto=Campaign, list_limit=5)
        self.__data_manager.create_fake_data([campaign])

        # act
        campaign_returned = self.__sut.load_by_id(id_=campaign.id)

        # assert
        assert campaign_returned == campaign

    def test_load_for_brand(self):
        # arrange
        brand = AutoFixture().create(dto=Brand, list_limit=5)
        campaigns = AutoFixture().create_many(dto=Campaign, list_limit=5, ammount=10)
        for campaign in campaigns:
            campaign.brand_id = brand.id
        self.__data_manager.create_fake_data([brand])
        self.__data_manager.create_fake_data(campaigns)

        # act
        returned_campaigns = self.__sut.load_for_auth_brand(auth_user_id=brand.auth_user_id)

        # assert
        assert campaigns == returned_campaigns

    def test_load_for_brand_when_brand_not_found(self):
        self.assertRaises(NotFoundException, lambda: self.__sut.load_for_auth_brand(auth_user_id="1234"))
