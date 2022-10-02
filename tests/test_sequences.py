from unittest import TestCase
from unittest.mock import Mock

from src.web.hooks import CommonBeforeHooks, UserBeforeHooks, CampaignBeforeHooks, CampaignAfterHooks, UserAfterHooks
from src.web.sequences import PreGenericUpdateCreateSubsequence, PreUpdateCreateCampaignSubsequence, \
    PostSingleCampaignSubsequence, PostMultipleCampaignSubsequence, PostSingleUserSubsequence, \
    PostMultipleUserSubsequence


class TestPreGenericUpdateCreateSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        common_before_hooks = CommonBeforeHooks(deserializer=Mock(),
                                                image_repo=Mock(),
                                                object_mapper=Mock(),
                                                logger=Mock())
        user_before_hooks = UserBeforeHooks(common_before_hooks=Mock(),
                                            logger=Mock())
        sut = PreGenericUpdateCreateSubsequence(common_before_hooks=common_before_hooks,
                                                user_before_hooks=user_before_hooks)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [common_before_hooks.set_body, user_before_hooks.set_auth_user_id])


class TestPreUpdateCreateCampaignSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        campaign_before_hooks = CampaignBeforeHooks(common_before_hooks=Mock(),
                                                    logger=Mock(),
                                                    campaign_validator=Mock())
        sut = PreUpdateCreateCampaignSubsequence(campaign_before_hooks=campaign_before_hooks)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [campaign_before_hooks.map_campaign_state,
                                              campaign_before_hooks.map_campaign_categories_and_values])


class TestPostSingleCampaignSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        campaign_after_hooks = CampaignAfterHooks(common_after_hooks=Mock(),
                                                  mapper=Mock())
        sut = PostSingleCampaignSubsequence(campaign_after_hooks=campaign_after_hooks)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [campaign_after_hooks.format_campaign_state,
                                              campaign_after_hooks.format_values_and_categories])


class TestPostMultipleCampaignSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        campaign_after_hooks = CampaignAfterHooks(common_after_hooks=Mock(),
                                                  mapper=Mock())
        sut = PostMultipleCampaignSubsequence(campaign_after_hooks=campaign_after_hooks)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [campaign_after_hooks.format_campaign_state_collection,
                                              campaign_after_hooks.format_values_and_categories_collection])


class TestPostSingleUserSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        user_after_hooks = UserAfterHooks(common_after_hooks=Mock(),
                                          mapper=Mock(),
                                          auth_user_repository=Mock())
        sut = PostSingleUserSubsequence(user_after_hooks=user_after_hooks)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [user_after_hooks.format_values_and_categories,
                                              user_after_hooks.tag_auth_user_claims_to_response])


class TestPostMultipleUserSubsequence(TestCase):

    def test_sequence(self):
        # arrange
        user_after_hooks = UserAfterHooks(common_after_hooks=Mock(),
                                          mapper=Mock(),
                                          auth_user_repository=Mock())
        sut = PostMultipleUserSubsequence(user_after_hooks=user_after_hooks)

        # act
        sut.build()

        # assert
        with self.subTest(msg="components match"):
            self.assertEqual(sut.components, [user_after_hooks.format_values_and_categories_collection,
                                              user_after_hooks.tag_auth_user_claims_to_response_collection])