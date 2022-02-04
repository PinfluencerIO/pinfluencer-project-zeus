from unittest import TestCase
from unittest.mock import Mock, MagicMock

from src.data.repositories import SqlAlchemyBrandRepository, SqlAlchemyInfluencerRepository
from src.exceptions import AlreadyExistsException, NotFoundException
from src.types import ImageRepository
from tests import InMemorySqliteDataManager, brand_generator, brand_dto_generator, TEST_DEFAULT_BRAND_LOGO, \
    TEST_DEFAULT_BRAND_HEADER_IMAGE, TEST_DEFAULT_INFLUENCER_PROFILE_IMAGE, influencer_dto_generator, \
    assert_brand_updatable_fields_are_equal


class BrandRepositoryTestCase(TestCase):

    def setUp(self):
        self._data_manager = InMemorySqliteDataManager()
        self._image_repository: ImageRepository = Mock()
        self._sut = SqlAlchemyBrandRepository(data_manager=self._data_manager,
                                              image_repository=self._image_repository)


class TestBaseRepository(BrandRepositoryTestCase):

    def test_load_by_id(self):
        expected_brand = brand_dto_generator(1)
        self._data_manager.create_fake_data([brand_generator(expected_brand)])
        actual_brand = self._sut.load_by_id(id_=expected_brand.id)
        assert expected_brand.__dict__ == actual_brand.__dict__

    def test_load_by_id_when_brand_cannot_be_found(self):
        self.assertRaises(NotFoundException, lambda: self._sut.load_by_id(id_="1234"))

    def test_load_collection(self):
        expected_brands = [brand_dto_generator(1), brand_dto_generator(2), brand_dto_generator(3)]
        self._data_manager.create_fake_data(list(map(lambda x: brand_generator(x), expected_brands)))
        actual_brands = self._sut.load_collection()
        assert list(map(lambda x: x.__dict__, expected_brands)) == list(map(lambda x: x.__dict__, actual_brands))

    def test_load_collection_when_no_brands_exist(self):
        actual_brands = self._sut.load_collection()
        assert [] == actual_brands


class TestUserRepository(BrandRepositoryTestCase):

    def test_load_for_auth_user(self):
        expected = brand_dto_generator(num=1)
        self._data_manager.create_fake_data([brand_generator(expected)])
        actual = self._sut.load_for_auth_user(auth_user_id="1234brand1")
        assert expected.__dict__ == actual.__dict__

    def test_load_for_auth_user_when_brand_not_found(self):
        self.assertRaises(NotFoundException, lambda: self._sut.load_for_auth_user(auth_user_id="1234brand1"))

    def test_write_new_for_auth_user(self):
        expected = brand_dto_generator(num=1)
        self._sut.write_new_for_auth_user(auth_user_id="1234brand1",
                                          payload=expected)
        actual = self._sut.load_by_id(id_=expected.id)
        assert actual.__dict__ == expected.__dict__

    def test_write_new_for_auth_user_when_already_exists(self):
        expected = brand_dto_generator(num=1)
        brand_to_create = brand_dto_generator(num=2)
        brand_to_create.auth_user_id = expected.auth_user_id
        self._data_manager.create_fake_data([brand_generator(expected)])
        self.assertRaises(AlreadyExistsException, lambda: self._sut.write_new_for_auth_user(auth_user_id="1234brand1",
                                                                                            payload=brand_to_create))
        actual = self._sut.load_for_auth_user(auth_user_id=brand_to_create.auth_user_id)
        assert actual.__dict__ != brand_to_create.__dict__


class TestBrandRepository(BrandRepositoryTestCase):

    def test_write_new_for_auth_user(self):
        expected = brand_dto_generator(num=1)
        self._sut.write_new_for_auth_user(auth_user_id="1234brand1",
                                          payload=expected)
        actual = self._sut.load_by_id(id_=expected.id)
        assert actual.logo == TEST_DEFAULT_BRAND_LOGO
        assert actual.header_image == TEST_DEFAULT_BRAND_HEADER_IMAGE

    def test_update_for_auth_user(self):
        existing_brand = brand_dto_generator(num=1)
        expected = brand_dto_generator(num=2)
        expected.auth_user_id = existing_brand.auth_user_id
        self._data_manager.create_fake_data([brand_generator(existing_brand)])
        self._sut.update_for_auth_user(auth_user_id=existing_brand.auth_user_id,
                                       payload=expected)
        actual = self._sut.load_by_id(id_=existing_brand.id)
        assert_brand_updatable_fields_are_equal(actual.__dict__, expected.__dict__)
        assert actual.values == expected.values
        assert actual.categories == expected.categories

    def test_update_for_auth_user_when_not_found(self):
        expected = brand_dto_generator(num=1)
        self.assertRaises(NotFoundException, lambda: self._sut.update_for_auth_user(auth_user_id=expected.auth_user_id,
                                                                                    payload=expected))

    def test_update_logo_for_auth_user(self):
        image_bytes = "bytes"
        brand = brand_dto_generator(num=1)
        expected_logo = "test.png"
        self._image_repository.upload = MagicMock(return_value=expected_logo)
        self._data_manager.create_fake_data([brand_generator(brand)])
        returned_brand = self._sut.update_logo_for_auth_user(auth_user_id=brand.auth_user_id,
                                            image_bytes=image_bytes)
        self._image_repository.upload.assert_called_once_with(path=brand.id,
                                                              image_base64_encoded=image_bytes)
        actual_logo = self._sut.load_by_id(id_=brand.id).logo
        assert returned_brand.logo == expected_logo == actual_logo

    def test_update_logo_for_auth_user_when_not_found(self):
        self.assertRaises(NotFoundException, lambda: self._sut.update_logo_for_auth_user(auth_user_id="12345",
                                                                                         image_bytes="imagebytes"))

    def test_update_header_image_for_auth_user(self):
        image_bytes = "bytes"
        brand = brand_dto_generator(num=1)
        expected_header_image = "test.png"
        self._image_repository.upload = MagicMock(return_value=expected_header_image)
        self._data_manager.create_fake_data([brand_generator(brand)])
        returned_brand = self._sut.update_header_image_for_auth_user(auth_user_id=brand.auth_user_id,
                                                            image_bytes=image_bytes)
        self._image_repository.upload.assert_called_once_with(path=brand.id,
                                                              image_base64_encoded=image_bytes)
        actual_header_image = self._sut.load_by_id(id_=brand.id).header_image
        assert returned_brand.header_image == expected_header_image == actual_header_image

    def test_update_header_image_for_auth_user_when_not_found(self):
        self.assertRaises(NotFoundException, lambda: self._sut.update_header_image_for_auth_user(auth_user_id="12345",
                                                                                                 image_bytes="imagebytes"))


class TestInfluencerRepository(TestCase):

    def setUp(self):
        self.__data_manager = InMemorySqliteDataManager()
        self.__image_repository = Mock()
        self.__sut = SqlAlchemyInfluencerRepository(data_manager=self.__data_manager,
                                                    image_repository=self.__image_repository)

    def test_write_new_for_auth_user(self):
        expected = influencer_dto_generator(num=1)
        self.__sut.write_new_for_auth_user(auth_user_id="1234brand1",
                                           payload=expected)
        actual = self.__sut.load_by_id(id_=expected.id)
        assert actual.image == TEST_DEFAULT_INFLUENCER_PROFILE_IMAGE
