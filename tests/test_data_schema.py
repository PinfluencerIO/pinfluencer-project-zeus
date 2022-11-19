from unittest import TestCase

from sqlalchemy import or_

from src.app import logger_factory
from src.crosscutting import AutoFixture
from src.data.entities import create_mappings
from src.domain.models import Brand, Value, Influencer, Category, Listing
from tests import InMemorySqliteDataManager


class TestBrandSchema(TestCase):

    def setUp(self) -> None:
        self.__sut = InMemorySqliteDataManager()
        create_mappings(logger=logger_factory())

    def test_update_brand_values(self):
        # arrange
        brand = AutoFixture().create(dto=Brand, list_limit=20)
        new_brand = AutoFixture().create(dto=Brand, list_limit=20)
        new_values_length = len(new_brand.values)
        self.__sut.create_fake_data([brand])

        # act
        brand_in_db = self.__sut.session.query(Brand).first()
        brand_in_db.values = new_brand.values
        self.__sut.session.commit()

        # assert
        with self.subTest(msg="values are same length as new values"):
            values = self.__sut.session.query(Value).all()
            self.assertEqual(len(values), new_values_length)

        # assert
        with self.subTest(msg="there are no values with no foreign key relationship"):
            values = self.__sut.session.query(Value).filter(or_(getattr(Value, 'brand_id') is None,
                                                                getattr(Value, 'influencer_id') is None,
                                                                getattr(Value, 'listing_id') is None)).all()
            self.assertEqual(len(values), 0)

    def test_update_brand_categories(self):
        # arrange
        brand = AutoFixture().create(dto=Brand, list_limit=20)
        new_brand = AutoFixture().create(dto=Brand, list_limit=20)
        new_categories_length = len(new_brand.categories)
        self.__sut.create_fake_data([brand])

        # act
        brand_in_db = self.__sut.session.query(Brand).first()
        brand_in_db.categories = new_brand.categories
        self.__sut.session.commit()

        # assert
        with self.subTest(msg="categories are same length as new values"):
            categories = self.__sut.session.query(Category).all()
            self.assertEqual(len(categories), new_categories_length)

        # assert
        with self.subTest(msg="there are no categories with no foreign key relationship"):
            categories = self.__sut.session.query(Category).filter(or_(getattr(Category, 'brand_id') is None,
                                                                       getattr(Category, 'influencer_id') is None,
                                                                       getattr(Category, 'listing_id') is None)).all()
            self.assertEqual(len(categories), 0)


class TestInfluencerSchema(TestCase):

    def setUp(self) -> None:
        self.__sut = InMemorySqliteDataManager()
        create_mappings(logger=logger_factory())

    def test_update_influencer_values(self):
        # arrange
        influencer = AutoFixture().create(dto=Influencer, list_limit=20)
        new_influencer = AutoFixture().create(dto=Influencer, list_limit=20)
        new_values_length = len(new_influencer.values)
        self.__sut.create_fake_data([influencer])

        # act
        influencer_in_db = self.__sut.session.query(Influencer).first()
        influencer_in_db.values = new_influencer.values
        self.__sut.session.commit()

        # assert
        with self.subTest(msg="values are same length as new values"):
            values = self.__sut.session.query(Value).all()
            self.assertEqual(len(values), new_values_length)

        # assert
        with self.subTest(msg="there are no values with no foreign key relationship"):
            values = self.__sut.session.query(Value).filter(or_(getattr(Value, 'brand_id') is None,
                                                                getattr(Value, 'influencer_id') is None,
                                                                getattr(Value, 'listing_id') is None)).all()
            self.assertEqual(len(values), 0)

    def test_update_influencer_categories(self):
        # arrange
        influencer = AutoFixture().create(dto=Influencer, list_limit=20)
        new_influencer = AutoFixture().create(dto=Influencer, list_limit=20)
        new_categories_length = len(new_influencer.categories)
        self.__sut.create_fake_data([influencer])

        # act
        influencer_in_db = self.__sut.session.query(Influencer).first()
        influencer_in_db.categories = new_influencer.categories
        self.__sut.session.commit()

        # assert
        with self.subTest(msg="categories are same length as new values"):
            categories = self.__sut.session.query(Category).all()
            self.assertEqual(len(categories), new_categories_length)

        # assert
        with self.subTest(msg="there are no categories with no foreign key relationship"):
            categories = self.__sut.session.query(Category).filter(or_(getattr(Category, 'brand_id') is None,
                                                                       getattr(Category, 'influencer_id') is None,
                                                                       getattr(Category, 'listing_id') is None)).all()
            self.assertEqual(len(categories), 0)


class TestListingSchema(TestCase):

    def setUp(self) -> None:
        self.__sut = InMemorySqliteDataManager()
        create_mappings(logger=logger_factory())

    def test_update_values(self):
        # arrange
        listing = AutoFixture().create(dto=Listing, list_limit=20)
        new_listing = AutoFixture().create(dto=Listing, list_limit=20)
        new_values_length = len(new_listing.values)
        self.__sut.create_fake_data([listing])

        # act
        listing_in_db = self.__sut.session.query(Listing).first()
        listing_in_db.values = new_listing.values
        self.__sut.session.commit()

        # assert
        with self.subTest(msg="values are same length as new values"):
            values = self.__sut.session.query(Value).all()
            self.assertEqual(len(values), new_values_length)

        # assert
        with self.subTest(msg="there are no values with no foreign key relationship"):
            values = self.__sut.session.query(Value).filter(or_(getattr(Value, 'brand_id') is None,
                                                                getattr(Value, 'influencer_id') is None,
                                                                getattr(Value, 'listing_id') is None)).all()
            self.assertEqual(len(values), 0)

    def test_update_categories(self):
        # arrange
        listing = AutoFixture().create(dto=Listing, list_limit=20)
        new_listing = AutoFixture().create(dto=Listing, list_limit=20)
        new_categories_length = len(new_listing.categories)
        self.__sut.create_fake_data([listing])

        # act
        listing_in_db = self.__sut.session.query(Listing).first()
        listing_in_db.categories = new_listing.categories
        self.__sut.session.commit()

        # assert
        with self.subTest(msg="categories are same length as new values"):
            categories = self.__sut.session.query(Category).all()
            self.assertEqual(len(categories), new_categories_length)

        # assert
        with self.subTest(msg="there are no categories with no foreign key relationship"):
            categories = self.__sut.session.query(Category).filter(or_(getattr(Category, 'brand_id') is None,
                                                                       getattr(Category, 'influencer_id') is None,
                                                                       getattr(Category, 'listing_id') is None)).all()
            self.assertEqual(len(categories), 0)