from unittest import TestCase
from unittest.mock import Mock

from simple_injection import ServiceCollection

from src.app import bootstrap
from src.web.controllers import CampaignController, InfluencerController
from src.web.hooks import CommonBeforeHooks, UserBeforeHooks, CampaignBeforeHooks, CampaignAfterHooks, UserAfterHooks, \
    BrandBeforeHooks, InfluencerBeforeHooks, InfluencerAfterHooks
from src.web.sequences import PreGenericUpdateCreateSubsequenceBuilder, PreUpdateCreateCampaignSubsequenceBuilder, \
    PostSingleCampaignSubsequenceBuilder, PostMultipleCampaignSubsequenceBuilder, PostSingleUserSubsequenceBuilder, \
    PostMultipleUserSubsequenceBuilder, UpdateImageForCampaignSequenceBuilder, UpdateCampaignSequenceBuilder, \
    CreateCampaignSequenceBuilder, GetCampaignByIdSequenceBuilder, GetCampaignsForBrandSequenceBuilder, \
    UpdateInfluencerImageSequenceBuilder, UpdateInfluencerSequenceBuilder, CreateInfluencerSequenceBuilder, \
    GetAuthInfluencerSequenceBuilder, GetInfluencerByIdSequenceBuilder, GetAllInfluencersSequenceBuilder


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


class TestPreUpdateCreateCampaignSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(PreUpdateCreateCampaignSubsequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [ioc.resolve(CampaignBeforeHooks).map_campaign_state,
                                              ioc.resolve(CampaignBeforeHooks).map_campaign_categories_and_values])


class TestPostSingleCampaignSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(PostSingleCampaignSubsequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [ioc.resolve(CampaignAfterHooks).format_campaign_state,
                                              ioc.resolve(CampaignAfterHooks).format_values_and_categories])


class TestPostMultipleCampaignSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(PostMultipleCampaignSubsequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [ioc.resolve(CampaignAfterHooks).format_campaign_state_collection,
                                              ioc.resolve(CampaignAfterHooks).format_values_and_categories_collection])


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
            self.assertEqual(sut.components, [ioc.resolve(UserAfterHooks).format_values_and_categories,
                                              ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response])


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
            self.assertEqual(sut.components, [ioc.resolve(UserAfterHooks).format_values_and_categories_collection,
                                              ioc.resolve(UserAfterHooks).tag_auth_user_claims_to_response_collection])


class TestUpdateImageForCampaignSequence(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateImageForCampaignSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(CampaignBeforeHooks).validate_id,
                                              ioc.resolve(BrandBeforeHooks).validate_auth_brand,
                                              ioc.resolve(CampaignBeforeHooks).validate_image_key,
                                              ioc.resolve(CampaignBeforeHooks).upload_image,
                                              ioc.resolve(CampaignController).update_campaign_image,
                                              ioc.resolve(PostSingleCampaignSubsequenceBuilder),
                                              ioc.resolve(CampaignAfterHooks).tag_bucket_url_to_images])


class TestUpdateCampaignSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(UpdateCampaignSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(CampaignBeforeHooks).validate_id,
                                              ioc.resolve(CampaignBeforeHooks).validate_campaign,
                                              ioc.resolve(BrandBeforeHooks).validate_auth_brand,
                                              ioc.resolve(CampaignBeforeHooks).map_campaign_state,
                                              ioc.resolve(CampaignBeforeHooks).map_campaign_categories_and_values,
                                              ioc.resolve(CampaignController).update_campaign,
                                              ioc.resolve(PostSingleCampaignSubsequenceBuilder),
                                              ioc.resolve(CampaignAfterHooks).tag_bucket_url_to_images])


class TestCreateCampaignSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(CreateCampaignSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(PreGenericUpdateCreateSubsequenceBuilder),
                                              ioc.resolve(CampaignBeforeHooks).validate_campaign,
                                              ioc.resolve(BrandBeforeHooks).validate_auth_brand,
                                              ioc.resolve(CampaignBeforeHooks).map_campaign_state,
                                              ioc.resolve(CampaignBeforeHooks).map_campaign_categories_and_values,
                                              ioc.resolve(CampaignController).create,
                                              ioc.resolve(PostSingleCampaignSubsequenceBuilder),
                                              ioc.resolve(CampaignAfterHooks).tag_bucket_url_to_images])


class TestGetCampaignByIdSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetCampaignByIdSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(CampaignBeforeHooks).validate_id,
                                              ioc.resolve(CampaignController).get_by_id,
                                              ioc.resolve(PostSingleCampaignSubsequenceBuilder),
                                              ioc.resolve(CampaignAfterHooks).tag_bucket_url_to_images])


class TestGetCampaignsForBrandSequenceBuilder(TestCase):

    def test_sequence(self):
        # arrange
        ioc = ServiceCollection()
        setup(ioc)
        sut = ioc.resolve(GetCampaignsForBrandSequenceBuilder)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.maxDiff = None
            self.assertEqual(sut.components, [ioc.resolve(UserBeforeHooks).set_auth_user_id,
                                              ioc.resolve(CampaignController).get_for_brand,
                                              ioc.resolve(PostMultipleCampaignSubsequenceBuilder),
                                              ioc.resolve(CampaignAfterHooks).tag_bucket_url_to_images_collection])


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
                                              ioc.resolve(InfluencerBeforeHooks).validate_influencer,
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