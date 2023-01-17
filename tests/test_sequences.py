from unittest import TestCase
from unittest.mock import Mock

from simple_injection import ServiceCollection

from src.app import bootstrap
from src.web.controllers import ListingController, InfluencerController, BrandController, NotificationController, \
    AudienceAgeController, AudienceGenderController, BrandListingController, CollaborationController
from src.web.hooks import CommonBeforeHooks, UserBeforeHooks, ListingBeforeHooks, ListingAfterHooks, UserAfterHooks, \
    BrandBeforeHooks, InfluencerBeforeHooks, InfluencerAfterHooks, BrandAfterHooks, NotificationBeforeHooks, \
    AudienceAgeBeforeHooks, AudienceAgeAfterHooks, AudienceGenderAfterHooks, AudienceGenderBeforeHooks, \
    InfluencerOnBoardingAfterHooks, CollaborationBeforeHooks
from src.web.sequences import PreGenericUpdateCreateSubsequenceBuilder, PreUpdateCreateListingSubsequenceBuilder, \
    PostSingleUserSubsequenceBuilder, \
    PostMultipleUserSubsequenceBuilder, UpdateImageForListingSequenceBuilder, UpdateListingSequenceBuilder, \
    CreateListingSequenceBuilder, GetListingByIdSequenceBuilder, GetListingsForBrandSequenceBuilder, \
    UpdateInfluencerImageSequenceBuilder, UpdateInfluencerSequenceBuilder, CreateInfluencerSequenceBuilder, \
    GetAuthInfluencerSequenceBuilder, GetInfluencerByIdSequenceBuilder, GetAllInfluencersSequenceBuilder, \
    UpdateBrandImageSequenceBuilder, UpdateBrandSequenceBuilder, CreateBrandSequenceBuilder, \
    GetAuthBrandSequenceBuilder, GetBrandByIdSequenceBuilder, GetAllBrandsSequenceBuilder, \
    CreateNotificationSequenceBuilder, GetNotificationByIdSequenceBuilder, CreateAudienceAgeSequenceBuilder, \
    GetAudienceAgeSequenceBuilder, UpdateAudienceAgeSequenceBuilder, CreateAudienceGenderSequenceBuilder, \
    GetAudienceGenderSequenceBuilder, UpdateAudienceGenderSequenceBuilder, CreateInfluencerProfileSequenceBuilder, \
    UpdateInfluencerProfileSequenceBuilder, GetInfluencerProfileSequenceBuilder, \
    GetBrandListingsForBrandSequenceBuilder, CreateCollaborationForInfluencerSequenceBuilder


def setup(ioc: ServiceCollection):
    mock_middleware_pipeline = Mock()
    bootstrap(event={"routeKey": "GET /brands"},
              context={},
              middleware=mock_middleware_pipeline,
              ioc=ioc,
              data_manager=Mock(),
              cognito_auth_service=Mock())

class TestPreGenericUpdateCreateSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [ioc.resolve(CommonBeforeHooks).set_body,
                                              ioc.resolve(UserBeforeHooks).set_auth_user_id])


class TestPreUpdateCreateListingSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(PreUpdateCreateListingSubsequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [ioc.resolve(ListingBeforeHooks).map_categories_and_values])


class TestPostSingleUserSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(PostSingleUserSubsequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response])


class TestPostMultipleUserSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(PostMultipleUserSubsequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response_collection])


class TestUpdateImageForListingSequence(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateImageForListingSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(ListingBeforeHooks).validate_id,
                                              ioc.resolve(BrandBeforeHooks).validate_auth_brand,
                                              ioc.resolve(ListingBeforeHooks).validate_image_key,
                                              ioc.resolve(ListingBeforeHooks).upload_image,
                                              ioc.resolve(ListingController).update_listing_image,
                                              ioc.resolve(ListingAfterHooks).tag_bucket_url_to_images])


class TestUpdateListingSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateListingSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(ListingBeforeHooks).validate_id,
                                              ioc.resolve(ListingBeforeHooks).validate_listing,
                                              ioc.resolve(BrandBeforeHooks).validate_auth_brand,
                                              ioc.resolve(ListingBeforeHooks).map_categories_and_values,
                                              ioc.resolve(ListingController).update_listing,
                                              ioc.resolve(ListingAfterHooks).tag_bucket_url_to_images])


class TestCreateListingSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(CreateListingSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(ListingBeforeHooks).validate_listing,
                                              ioc.resolve(BrandBeforeHooks).validate_auth_brand,
                                              ioc.resolve(ListingBeforeHooks).map_categories_and_values,
                                              ioc.resolve(ListingController).create_for_brand,
                                              ioc.resolve(ListingAfterHooks).save_state,
                                              ioc.resolve(ListingAfterHooks).tag_bucket_url_to_images])


class TestGetListingByIdSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetListingByIdSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(ListingBeforeHooks).validate_id,
                                              ioc.resolve(ListingController).get_by_id,
                                              ioc.resolve(ListingAfterHooks).tag_bucket_url_to_images])


class TestGetListingsForBrandSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetListingsForBrandSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                              ioc.resolve(BrandBeforeHooks).validate_auth_brand,
                                              ioc.resolve(ListingController).get_for_brand,
                                              ioc.resolve(ListingAfterHooks).tag_bucket_url_to_images_collection])


class TestUpdateImageForInfluencerSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateInfluencerImageSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(InfluencerBeforeHooks).validate_image_key,
                                              ioc.resolve(InfluencerBeforeHooks).upload_image,
                                              ioc.resolve(InfluencerController).update_image_field_for_user,
                                              ioc.resolve(PostSingleUserSubsequenceBuilder),
                                              ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images])


class TestUpdateInfluencerSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateInfluencerSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(UserBeforeHooks).set_categories_and_values,
                                              ioc.resolve(InfluencerBeforeHooks).validate_influencer,
                                              ioc.resolve(InfluencerController).update_for_user,
                                              ioc.resolve(InfluencerAfterHooks).set_influencer_claims,
                                              ioc.resolve(PostSingleUserSubsequenceBuilder),
                                              ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images])


class TestCreateInfluencerSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(CreateInfluencerSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(UserBeforeHooks).set_categories_and_values,
                                              ioc.resolve(InfluencerController).create,
                                              ioc.resolve(InfluencerAfterHooks).set_influencer_claims,
                                              ioc.resolve(PostSingleUserSubsequenceBuilder),
                                              ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images])


class TestGetAuthInfluencerSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetAuthInfluencerSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                              ioc.resolve(InfluencerController).get,
                                              ioc.resolve(PostSingleUserSubsequenceBuilder),
                                              ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images])


class TestGetInfluencerByIdSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetInfluencerByIdSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(InfluencerBeforeHooks).validate_uuid,
                                              ioc.resolve(InfluencerController).get_by_id,
                                              ioc.resolve(PostSingleUserSubsequenceBuilder),
                                              ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images])


class TestGetAllInfluencersSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetAllInfluencersSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(InfluencerController).get_all,
                                              ioc.resolve(PostMultipleUserSubsequenceBuilder),
                                              ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images_collection])


class TestUpdateBrandImageSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateBrandImageSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(BrandBeforeHooks).validate_image_key,
                                              ioc.resolve(BrandBeforeHooks).upload_image,
                                              ioc.resolve(BrandController).update_image_field_for_user,
                                              ioc.resolve(PostSingleUserSubsequenceBuilder),
                                              ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images])


class TestUpdateBrandSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateBrandSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(UserBeforeHooks).set_categories_and_values,
                                              ioc.resolve(BrandBeforeHooks).validate_brand,
                                              ioc.resolve(BrandController).update_for_user,
                                              ioc.resolve(BrandAfterHooks).set_brand_claims,
                                              ioc.resolve(PostSingleUserSubsequenceBuilder),
                                              ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images])


class TestCreateBrandSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(CreateBrandSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(UserBeforeHooks).set_categories_and_values,
                                              # ioc.resolve(BrandBeforeHooks).validate_brand,
                                              ioc.resolve(BrandController).create,
                                              ioc.resolve(BrandAfterHooks).set_brand_claims,
                                              ioc.resolve(PostSingleUserSubsequenceBuilder),
                                              ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images])


class TestGetAuthBrandSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetAuthBrandSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                              ioc.resolve(BrandController).get,
                                              ioc.resolve(PostSingleUserSubsequenceBuilder),
                                              ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images])


class TestGetBrandByIdSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetBrandByIdSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(BrandBeforeHooks).validate_uuid,
                                              ioc.resolve(BrandController).get_by_id,
                                              ioc.resolve(PostSingleUserSubsequenceBuilder),
                                              ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images])


class TestGetAllBrandsSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetAllBrandsSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(BrandController).get_all,
                                              ioc.resolve(PostMultipleUserSubsequenceBuilder),
                                              ioc.resolve(BrandAfterHooks).tag_bucket_url_to_images_collection])


class TestCreateNotificationSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(CreateNotificationSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(NotificationBeforeHooks).override_create_fields,
                                              ioc.resolve(NotificationController).create])


class TestGetNotificationByIdSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetNotificationByIdSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(NotificationBeforeHooks).validate_uuid,
                ioc.resolve(NotificationController).get_by_id
            ])

class TestCreateAudienceAgeSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(CreateAudienceAgeSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                ioc.resolve(AudienceAgeBeforeHooks).check_audience_ages_are_empty,
                ioc.resolve(InfluencerBeforeHooks).validate_auth_influencer,
                ioc.resolve(AudienceAgeController).create_for_influencer,
                ioc.resolve(AudienceAgeAfterHooks).save_state,
            ])


class TestGetAudienceAgeSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetAudienceAgeSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(UserBeforeHooks).set_auth_user_id,
                ioc.resolve(InfluencerBeforeHooks).validate_auth_influencer,
                ioc.resolve(AudienceAgeController).get_for_influencer
            ])


class TestUpdateAudienceAgeSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateAudienceAgeSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                ioc.resolve(InfluencerBeforeHooks).validate_auth_influencer,
                ioc.resolve(AudienceAgeController).update_for_influencer,
                ioc.resolve(AudienceAgeAfterHooks).save_state
            ])


class TestCreateAudienceGenderSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(CreateAudienceGenderSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                ioc.resolve(AudienceGenderBeforeHooks).check_audience_genders_are_empty,
                ioc.resolve(InfluencerBeforeHooks).validate_auth_influencer,
                ioc.resolve(AudienceGenderController).create_for_influencer,
                ioc.resolve(AudienceGenderAfterHooks).save_state,
            ])


class TestGetAudienceGenderSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetAudienceGenderSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(UserBeforeHooks).set_auth_user_id,
                ioc.resolve(InfluencerBeforeHooks).validate_auth_influencer,
                ioc.resolve(AudienceGenderController).get_for_influencer
            ])


class TestUpdateAudienceGenderSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateAudienceGenderSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                ioc.resolve(InfluencerBeforeHooks).validate_auth_influencer,
                ioc.resolve(AudienceGenderController).update_for_influencer,
                ioc.resolve(AudienceGenderAfterHooks).save_state
            ])


class TestCreateInfluencerProfileSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(CreateInfluencerProfileSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                ioc.resolve(AudienceGenderBeforeHooks).check_audience_genders_are_empty,
                ioc.resolve(AudienceGenderController).create_for_influencer,
                ioc.resolve(InfluencerOnBoardingAfterHooks).cache_audience_gender_data,
                ioc.resolve(AudienceAgeBeforeHooks).check_audience_ages_are_empty,
                ioc.resolve(AudienceAgeController).create_for_influencer,
                ioc.resolve(InfluencerOnBoardingAfterHooks).cache_audience_age_data,
                ioc.resolve(UserBeforeHooks).set_categories_and_values,
                ioc.resolve(InfluencerController).create,
                ioc.resolve(InfluencerOnBoardingAfterHooks).cache_influencer_data,
                ioc.resolve(InfluencerOnBoardingAfterHooks).merge_influencer_cache,
                ioc.resolve(InfluencerAfterHooks).set_influencer_claims,
                ioc.resolve(PostSingleUserSubsequenceBuilder),
                ioc.resolve(InfluencerAfterHooks).tag_bucket_url_to_images
            ])


class TestUpdateInfluencerProfileSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateInfluencerProfileSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                ioc.resolve(AudienceGenderController).update_for_influencer,
                ioc.resolve(InfluencerOnBoardingAfterHooks).cache_audience_gender_data,
                ioc.resolve(AudienceAgeController).update_for_influencer,
                ioc.resolve(InfluencerOnBoardingAfterHooks).cache_audience_age_data,
                ioc.resolve(UserBeforeHooks).set_categories_and_values,
                ioc.resolve(InfluencerBeforeHooks).validate_influencer,
                ioc.resolve(InfluencerController).update_for_user,
                ioc.resolve(InfluencerOnBoardingAfterHooks).cache_influencer_data,
                ioc.resolve(InfluencerOnBoardingAfterHooks).merge_influencer_cache,
                ioc.resolve(InfluencerAfterHooks).set_influencer_claims,
                ioc.resolve(PostSingleUserSubsequenceBuilder),
            ])


class TestGetInfluencerProfileSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetInfluencerProfileSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(UserBeforeHooks).set_auth_user_id,
                ioc.resolve(AudienceGenderController).get_for_influencer,
                ioc.resolve(InfluencerOnBoardingAfterHooks).cache_audience_gender_data,
                ioc.resolve(AudienceAgeController).get_for_influencer,
                ioc.resolve(InfluencerOnBoardingAfterHooks).cache_audience_age_data,
                ioc.resolve(InfluencerController).get,
                ioc.resolve(InfluencerOnBoardingAfterHooks).cache_influencer_data,
                ioc.resolve(InfluencerOnBoardingAfterHooks).merge_influencer_cache,
                ioc.resolve(PostSingleUserSubsequenceBuilder)
            ])


class TestGetBrandListingsForBrandSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetBrandListingsForBrandSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(UserBeforeHooks).set_auth_user_id,
                ioc.resolve(BrandBeforeHooks).validate_brand,
                ioc.resolve(BrandListingController).get_for_brand,
                ioc.resolve(ListingAfterHooks).tag_bucket_url_to_images_collection
            ])


class TestCreateCollaborationForInfluencerSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(CreateCollaborationForInfluencerSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [
                ioc.resolve(CommonBeforeHooks).set_body,
                ioc.resolve(UserBeforeHooks).set_auth_user_id,
                ioc.resolve(CollaborationBeforeHooks).load_brand_from_listing_to_request_body,
                ioc.resolve(CollaborationController).create_for_influencer
            ])