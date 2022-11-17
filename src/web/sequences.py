from src.web import FluentSequenceBuilder, PinfluencerContext
from src.web.controllers import CampaignController, InfluencerController, BrandController, NotificationController, \
    AudienceAgeController, AudienceGenderController
from src.web.hooks import CommonBeforeHooks, CampaignBeforeHooks, CampaignAfterHooks, UserAfterHooks, UserBeforeHooks, \
    BrandBeforeHooks, BrandAfterHooks, InfluencerBeforeHooks, InfluencerAfterHooks, NotificationBeforeHooks, \
    AudienceAgeBeforeHooks, CommonAfterHooks, AudienceAgeAfterHooks, AudienceGenderAfterHooks, AudienceGenderBeforeHooks


class PreGenericUpdateCreateSubsequenceBuilder(FluentSequenceBuilder):

    def __init__(self, common_before_hooks: CommonBeforeHooks,
                 user_before_hooks: UserBeforeHooks):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__common_before_hooks = common_before_hooks

    def build(self):
        self._add_command(self.__common_before_hooks.set_body)\
            ._add_command(self.__user_before_hooks.set_auth_user_id)


class PreUpdateCreateCampaignSubsequenceBuilder(FluentSequenceBuilder):

    def __init__(self, campaign_before_hooks: CampaignBeforeHooks):
        super().__init__()
        self.__campaign_before_hooks = campaign_before_hooks

    def build(self):
        self._add_command(self.__campaign_before_hooks.map_campaign_state) \
            ._add_command(self.__campaign_before_hooks.map_campaign_categories_and_values)


class PostSingleCampaignSubsequenceBuilder(FluentSequenceBuilder):

    def __init__(self, campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
        self.__campaign_after_hooks = campaign_after_hooks

    def build(self):
        self._add_command(self.__campaign_after_hooks.format_campaign_state) \
            ._add_command(self.__campaign_after_hooks.format_values_and_categories)


class PostMultipleCampaignSubsequenceBuilder(FluentSequenceBuilder):

    def __init__(self, campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
        self.__campaign_after_hooks = campaign_after_hooks

    def build(self):
        self._add_command(self.__campaign_after_hooks.format_campaign_state_collection) \
            ._add_command(self.__campaign_after_hooks.format_values_and_categories_collection)


class PostSingleUserSubsequenceBuilder(FluentSequenceBuilder):

    def __init__(self, user_after_hooks: UserAfterHooks):
        super().__init__()
        self.__user_after_hooks = user_after_hooks

    def build(self):
        self._add_command(self.__user_after_hooks.format_values_and_categories) \
            ._add_command(self.__user_after_hooks.tag_auth_user_claims_to_response)


class PostMultipleUserSubsequenceBuilder(FluentSequenceBuilder):

    def __init__(self, user_after_hooks: UserAfterHooks):
        super().__init__()
        self.__user_after_hooks = user_after_hooks

    def build(self):
        self._add_command(self.__user_after_hooks.format_values_and_categories_collection) \
            ._add_command(self.__user_after_hooks.tag_auth_user_claims_to_response_collection)


class UpdateImageForCampaignSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 campaign_before_hooks: CampaignBeforeHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 campaign_controller: CampaignController,
                 generic_update_sequence: PreGenericUpdateCreateSubsequenceBuilder,
                 post_single_campaign_sequence: PostSingleCampaignSubsequenceBuilder,
                 campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
        self.__campaign_after_hooks = campaign_after_hooks
        self.__post_single_campaign_sequence = post_single_campaign_sequence
        self.__generic_update_sequence = generic_update_sequence
        self.__campaign_controller = campaign_controller
        self.__brand_before_hooks = brand_before_hooks
        self.__campaign_before_hooks = campaign_before_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__generic_update_sequence)\
            ._add_command(command=self.__campaign_before_hooks.validate_id) \
            ._add_command(command=self.__brand_before_hooks.validate_auth_brand) \
            ._add_command(command=self.__campaign_before_hooks.validate_image_key) \
            ._add_command(command=self.__campaign_before_hooks.upload_image)\
            ._add_command(command=self.__campaign_controller.update_campaign_image) \
            ._add_sequence_builder(sequence_builder=self.__post_single_campaign_sequence)\
            ._add_command(command=self.__campaign_after_hooks.tag_bucket_url_to_images)


class UpdateCampaignSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 campaign_before_hooks: CampaignBeforeHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 campaign_controller: CampaignController,
                 generic_update_sequence: PreGenericUpdateCreateSubsequenceBuilder,
                 post_single_campaign_sequence: PostSingleCampaignSubsequenceBuilder,
                 campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
        self.__campaign_after_hooks = campaign_after_hooks
        self.__post_single_campaign_sequence = post_single_campaign_sequence
        self.__generic_update_sequence = generic_update_sequence
        self.__brand_before_hooks = brand_before_hooks
        self.__campaign_controller = campaign_controller
        self.__campaign_before_hooks = campaign_before_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__generic_update_sequence)\
            ._add_command(command=self.__campaign_before_hooks.validate_id)\
            ._add_command(command=self.__campaign_before_hooks.validate_campaign)\
            ._add_command(command=self.__brand_before_hooks.validate_auth_brand) \
            ._add_command(command=self.__campaign_before_hooks.map_campaign_state) \
            ._add_command(command=self.__campaign_before_hooks.map_campaign_categories_and_values) \
            ._add_command(command=self.__campaign_controller.update_campaign)\
            ._add_sequence_builder(sequence_builder=self.__post_single_campaign_sequence)\
            ._add_command(command=self.__campaign_after_hooks.tag_bucket_url_to_images)


class CreateCampaignSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 campaign_before_hooks: CampaignBeforeHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 campaign_controller: CampaignController,
                 generic_update_sequence: PreGenericUpdateCreateSubsequenceBuilder,
                 post_single_campaign_sequence: PostSingleCampaignSubsequenceBuilder,
                 common_after_hooks: CommonAfterHooks,
                 campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
        self.__common_after_hooks = common_after_hooks
        self.__campaign_after_hooks = campaign_after_hooks
        self.__post_single_campaign_sequence = post_single_campaign_sequence
        self.__generic_update_sequence = generic_update_sequence
        self.__brand_before_hooks = brand_before_hooks
        self.__campaign_controller = campaign_controller
        self.__campaign_before_hooks = campaign_before_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__generic_update_sequence) \
            ._add_command(command=self.__campaign_before_hooks.validate_campaign) \
            ._add_command(command=self.__brand_before_hooks.validate_auth_brand) \
            ._add_command(command=self.__campaign_before_hooks.map_campaign_state) \
            ._add_command(command=self.__campaign_before_hooks.map_campaign_categories_and_values) \
            ._add_command(command=self.__campaign_controller.create_for_brand) \
            ._add_command(command=self.__campaign_after_hooks.save_state) \
            ._add_sequence_builder(sequence_builder=self.__post_single_campaign_sequence) \
            ._add_command(command=self.__campaign_after_hooks.tag_bucket_url_to_images)


class GetCampaignByIdSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 campaign_before_hooks: CampaignBeforeHooks,
                 campaign_controller: CampaignController,
                 post_single_campaign_sequence: PostSingleCampaignSubsequenceBuilder,
                 campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
        self.__campaign_after_hooks = campaign_after_hooks
        self.__post_single_campaign_sequence = post_single_campaign_sequence
        self.__campaign_controller = campaign_controller
        self.__campaign_before_hooks = campaign_before_hooks

    def build(self):
        self._add_command(command=self.__campaign_before_hooks.validate_id) \
            ._add_command(command=self.__campaign_controller.get_by_id)\
            ._add_sequence_builder(sequence_builder=self.__post_single_campaign_sequence)\
            ._add_command(command=self.__campaign_after_hooks.tag_bucket_url_to_images)


class GetCampaignsForBrandSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 user_before_hooks: UserBeforeHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 campaign_controller: CampaignController,
                 post_multiple_campaign_sequence: PostMultipleCampaignSubsequenceBuilder,
                 campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
        self.__brand_before_hooks = brand_before_hooks
        self.__post_multiple_campaign_sequence = post_multiple_campaign_sequence
        self.__campaign_after_hooks = campaign_after_hooks
        self.__campaign_controller = campaign_controller
        self.__user_before_hooks = user_before_hooks

    def build(self):
        self._add_command(command=self.__user_before_hooks.set_auth_user_id) \
            ._add_command(command=self.__brand_before_hooks.validate_auth_brand) \
            ._add_command(command=self.__campaign_controller.get_for_brand) \
            ._add_sequence_builder(sequence_builder=self.__post_multiple_campaign_sequence) \
            ._add_command(command=self.__campaign_after_hooks.tag_bucket_url_to_images_collection)


class UpdateInfluencerImageSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, pre_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 influencer_controller: InfluencerController,
                 influencer_after_hooks: InfluencerAfterHooks,
                 post_user_single_sequence_builder: PostSingleUserSubsequenceBuilder):
        super().__init__()
        self.__post_user_single_sequence_builder = post_user_single_sequence_builder
        self.__influencer_after_hooks = influencer_after_hooks
        self.__influencer_controller = influencer_controller
        self.__influencer_before_hooks = influencer_before_hooks
        self.__pre_update_create_subsequence_builder = pre_update_create_subsequence_builder

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_update_create_subsequence_builder)\
            ._add_command(command=self.__influencer_before_hooks.validate_image_key) \
            ._add_command(command=self.__influencer_before_hooks.upload_image) \
            ._add_command(command=self.__influencer_controller.update_image_field_for_user) \
            ._add_sequence_builder(sequence_builder=self.__post_user_single_sequence_builder) \
            ._add_command(command=self.__influencer_after_hooks.tag_bucket_url_to_images)


class UpdateInfluencerSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, pre_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 influencer_controller: InfluencerController,
                 influencer_after_hooks: InfluencerAfterHooks,
                 post_user_single_sequence_builder: PostSingleUserSubsequenceBuilder,
                 user_before_hooks: UserBeforeHooks):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__post_user_single_sequence_builder = post_user_single_sequence_builder
        self.__influencer_after_hooks = influencer_after_hooks
        self.__influencer_controller = influencer_controller
        self.__influencer_before_hooks = influencer_before_hooks
        self.__pre_update_create_subsequence_builder = pre_update_create_subsequence_builder

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_update_create_subsequence_builder)\
            ._add_command(command=self.__user_before_hooks.set_categories_and_values) \
            ._add_command(command=self.__influencer_before_hooks.validate_influencer) \
            ._add_command(command=self.__influencer_controller.update_for_user) \
            ._add_command(command=self.__influencer_after_hooks.set_influencer_claims) \
            ._add_sequence_builder(sequence_builder=self.__post_user_single_sequence_builder) \
            ._add_command(command=self.__influencer_after_hooks.tag_bucket_url_to_images)


class CreateInfluencerSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, pre_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 influencer_controller: InfluencerController,
                 influencer_after_hooks: InfluencerAfterHooks,
                 post_user_single_sequence_builder: PostSingleUserSubsequenceBuilder,
                 user_before_hooks: UserBeforeHooks):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__post_user_single_sequence_builder = post_user_single_sequence_builder
        self.__influencer_after_hooks = influencer_after_hooks
        self.__influencer_controller = influencer_controller
        self.__influencer_before_hooks = influencer_before_hooks
        self.__pre_update_create_subsequence_builder = pre_update_create_subsequence_builder

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_update_create_subsequence_builder) \
            ._add_command(command=self.__user_before_hooks.set_categories_and_values) \
            ._add_command(command=self.__influencer_controller.create) \
            ._add_command(command=self.__influencer_after_hooks.set_influencer_claims) \
            ._add_sequence_builder(sequence_builder=self.__post_user_single_sequence_builder) \
            ._add_command(command=self.__influencer_after_hooks.tag_bucket_url_to_images)


class GetAuthInfluencerSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, influencer_controller: InfluencerController,
                 influencer_after_hooks: InfluencerAfterHooks,
                 post_user_single_sequence_builder: PostSingleUserSubsequenceBuilder,
                 user_before_hooks: UserBeforeHooks):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__post_user_single_sequence_builder = post_user_single_sequence_builder
        self.__influencer_after_hooks = influencer_after_hooks
        self.__influencer_controller = influencer_controller

    def build(self):
        self._add_command(command=self.__user_before_hooks.set_auth_user_id) \
            ._add_command(command=self.__influencer_controller.get) \
            ._add_sequence_builder(sequence_builder=self.__post_user_single_sequence_builder) \
            ._add_command(command=self.__influencer_after_hooks.tag_bucket_url_to_images)


class GetInfluencerByIdSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, influencer_controller: InfluencerController,
                 influencer_after_hooks: InfluencerAfterHooks,
                 post_user_single_sequence_builder: PostSingleUserSubsequenceBuilder,
                 influencer_before_hooks: InfluencerBeforeHooks):
        super().__init__()
        self.__influencer_before_hooks = influencer_before_hooks
        self.__post_user_single_sequence_builder = post_user_single_sequence_builder
        self.__influencer_after_hooks = influencer_after_hooks
        self.__influencer_controller = influencer_controller

    def build(self):
        self._add_command(command=self.__influencer_before_hooks.validate_uuid) \
            ._add_command(command=self.__influencer_controller.get_by_id) \
            ._add_sequence_builder(sequence_builder=self.__post_user_single_sequence_builder) \
            ._add_command(command=self.__influencer_after_hooks.tag_bucket_url_to_images)


class GetAllInfluencersSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 influencer_controller: InfluencerController,
                 influencer_after_hooks: InfluencerAfterHooks,
                 post_user_multiple_sequence_builder: PostMultipleUserSubsequenceBuilder):
        super().__init__()
        self.__post_user_multiple_sequence_builder = post_user_multiple_sequence_builder
        self.__influencer_after_hooks = influencer_after_hooks
        self.__influencer_controller = influencer_controller

    def build(self):
        self._add_command(command=self.__influencer_controller.get_all)\
            ._add_sequence_builder(sequence_builder=self.__post_user_multiple_sequence_builder) \
            ._add_command(command=self.__influencer_after_hooks.tag_bucket_url_to_images_collection)


class UpdateBrandImageSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, pre_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 brand_before_hooks: BrandBeforeHooks,
                 brand_controller: BrandController,
                 brand_after_hooks: BrandAfterHooks,
                 post_single_user_subsequence_builder: PostSingleUserSubsequenceBuilder):
        super().__init__()
        self.__post_single_user_subsequence_builder = post_single_user_subsequence_builder
        self.__brand_after_hooks = brand_after_hooks
        self.__brand_controller = brand_controller
        self.__brand_before_hooks = brand_before_hooks
        self.__pre_update_create_subsequence_builder = pre_update_create_subsequence_builder

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_update_create_subsequence_builder)\
            ._add_command(command=self.__brand_before_hooks.validate_image_key)\
            ._add_command(command=self.__brand_before_hooks.upload_image)\
            ._add_command(command=self.__brand_controller.update_image_field_for_user) \
            ._add_sequence_builder(sequence_builder=self.__post_single_user_subsequence_builder)\
            ._add_command(command=self.__brand_after_hooks.tag_bucket_url_to_images)


class UpdateBrandSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, pre_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 brand_before_hooks: BrandBeforeHooks,
                 brand_controller: BrandController,
                 brand_after_hooks: BrandAfterHooks,
                 user_before_hooks: UserBeforeHooks,
                 post_single_user_subsequence_builder: PostSingleUserSubsequenceBuilder):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__post_single_user_subsequence_builder = post_single_user_subsequence_builder
        self.__brand_after_hooks = brand_after_hooks
        self.__brand_controller = brand_controller
        self.__brand_before_hooks = brand_before_hooks
        self.__pre_update_create_subsequence_builder = pre_update_create_subsequence_builder

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_update_create_subsequence_builder)\
            ._add_command(command=self.__user_before_hooks.set_categories_and_values) \
            ._add_command(command=self.__brand_before_hooks.validate_brand) \
            ._add_command(command=self.__brand_controller.update_for_user) \
            ._add_command(command=self.__brand_after_hooks.set_brand_claims)\
            ._add_sequence_builder(sequence_builder=self.__post_single_user_subsequence_builder) \
            ._add_command(command=self.__brand_after_hooks.tag_bucket_url_to_images)


class CreateBrandSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, pre_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 brand_before_hooks: BrandBeforeHooks,
                 brand_controller: BrandController,
                 brand_after_hooks: BrandAfterHooks,
                 user_before_hooks: UserBeforeHooks,
                 post_single_user_subsequence_builder: PostSingleUserSubsequenceBuilder):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__post_single_user_subsequence_builder = post_single_user_subsequence_builder
        self.__brand_after_hooks = brand_after_hooks
        self.__brand_controller = brand_controller
        self.__brand_before_hooks = brand_before_hooks
        self.__pre_update_create_subsequence_builder = pre_update_create_subsequence_builder

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_update_create_subsequence_builder)\
            ._add_command(command=self.__user_before_hooks.set_categories_and_values) \
            ._add_command(command=self.__brand_controller.create) \
            ._add_command(command=self.__brand_after_hooks.set_brand_claims)\
            ._add_sequence_builder(sequence_builder=self.__post_single_user_subsequence_builder) \
            ._add_command(command=self.__brand_after_hooks.tag_bucket_url_to_images)


class GetAuthBrandSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, brand_controller: BrandController,
                 brand_after_hooks: BrandAfterHooks,
                 user_before_hooks: UserBeforeHooks,
                 post_single_user_subsequence_builder: PostSingleUserSubsequenceBuilder):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__post_single_user_subsequence_builder = post_single_user_subsequence_builder
        self.__brand_after_hooks = brand_after_hooks
        self.__brand_controller = brand_controller

    def build(self):
        self._add_command(command=self.__user_before_hooks.set_auth_user_id)\
            ._add_command(command=self.__brand_controller.get) \
            ._add_sequence_builder(sequence_builder=self.__post_single_user_subsequence_builder)\
            ._add_command(command=self.__brand_after_hooks.tag_bucket_url_to_images)


class GetBrandByIdSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, brand_controller: BrandController,
                 brand_after_hooks: BrandAfterHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 post_single_user_subsequence_builder: PostSingleUserSubsequenceBuilder):
        super().__init__()
        self.__brand_before_hooks = brand_before_hooks
        self.__post_single_user_subsequence_builder = post_single_user_subsequence_builder
        self.__brand_after_hooks = brand_after_hooks
        self.__brand_controller = brand_controller

    def build(self):
        self._add_command(command=self.__brand_before_hooks.validate_uuid)\
            ._add_command(command=self.__brand_controller.get_by_id)\
            ._add_sequence_builder(sequence_builder=self.__post_single_user_subsequence_builder)\
            ._add_command(command=self.__brand_after_hooks.tag_bucket_url_to_images)


class GetAllBrandsSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, brand_controller: BrandController,
                 brand_after_hooks: BrandAfterHooks,
                 post_multiple_user_subsequence_builder: PostMultipleUserSubsequenceBuilder):
        super().__init__()
        self.__post_multiple_user_subsequence_builder = post_multiple_user_subsequence_builder
        self.__brand_after_hooks = brand_after_hooks
        self.__brand_controller = brand_controller

    def build(self):
        self._add_command(command=self.__brand_controller.get_all)\
            ._add_sequence_builder(sequence_builder=self.__post_multiple_user_subsequence_builder)\
            ._add_command(command=self.__brand_after_hooks.tag_bucket_url_to_images_collection)


class CreateNotificationSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, pre_generic_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 notification_controller: NotificationController,
                 notification_before_hooks: NotificationBeforeHooks):
        super().__init__()
        self.__notification_before_hooks = notification_before_hooks
        self.__notification_controller = notification_controller
        self.__pre_generic_update_create_subsequence_builder = pre_generic_update_create_subsequence_builder

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_generic_update_create_subsequence_builder)\
            ._add_command(command=self.__notification_before_hooks.override_create_fields)\
            ._add_command(command=self.__notification_controller.create)


class GetNotificationByIdSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, notification_controller: NotificationController,
                 notification_before_hooks: NotificationBeforeHooks):
        super().__init__()
        self.__notification_before_hooks = notification_before_hooks
        self.__notification_controller = notification_controller

    def build(self):
        self._add_command(command=self.__notification_before_hooks.validate_uuid)\
            ._add_command(command=self.__notification_controller.get_by_id)


class CreateAudienceAgeSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 audience_age_controller: AudienceAgeController,
                 pre_generic_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 audience_age_before_hooks: AudienceAgeBeforeHooks,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 audience_age_after_hooks: AudienceAgeAfterHooks):
        super().__init__()
        self.__audience_age_before_hooks = audience_age_before_hooks
        self.__pre_generic_update_create_subsequence_builder = pre_generic_update_create_subsequence_builder
        self.__audience_age_controller = audience_age_controller
        self.__influencer_before_hooks = influencer_before_hooks
        self.__audience_age_after_hooks = audience_age_after_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_generic_update_create_subsequence_builder) \
            ._add_command(command=self.__audience_age_before_hooks.check_audience_ages_are_empty) \
            ._add_command(command=self.__influencer_before_hooks.validate_auth_influencer) \
            ._add_command(command=self.__audience_age_controller.create_for_influencer) \
            ._add_command(command=self.__audience_age_after_hooks.save_state)


class GetAudienceAgeSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 user_before_hooks: UserBeforeHooks,
                 audience_age_controller: AudienceAgeController,
                 influencer_before_hooks: InfluencerBeforeHooks):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__influencer_before_hooks = influencer_before_hooks
        self.__audience_age_controller = audience_age_controller

    def build(self):
        self._add_command(command=self.__user_before_hooks.set_auth_user_id) \
            ._add_command(command=self.__influencer_before_hooks.validate_auth_influencer)\
            ._add_command(command=self.__audience_age_controller.get_for_influencer)


class CreateAudienceGenderSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 audience_gender_controller: AudienceGenderController,
                 pre_generic_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 audience_gender_before_hooks: AudienceGenderBeforeHooks,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 audience_gender_after_hooks: AudienceGenderAfterHooks
                 ):
        super().__init__()
        self.__audience_gender_after_hooks = audience_gender_after_hooks
        self.__influencer_before_hooks = influencer_before_hooks
        self.__audience_gender_before_hooks = audience_gender_before_hooks
        self.__pre_generic_update_create_subsequence_builder = pre_generic_update_create_subsequence_builder
        self.__audience_gender_controller = audience_gender_controller

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_generic_update_create_subsequence_builder) \
            ._add_command(command=self.__audience_gender_before_hooks.check_audience_genders_are_empty) \
            ._add_command(command=self.__influencer_before_hooks.validate_auth_influencer) \
            ._add_command(command=self.__audience_gender_controller.create_for_influencer) \
            ._add_command(command=self.__audience_gender_after_hooks.save_state)


class UpdateAudienceAgeSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 audience_age_controller: AudienceAgeController,
                 pre_generic_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 audience_age_after_hooks: AudienceAgeAfterHooks):
        super().__init__()
        self.__pre_generic_update_create_subsequence_builder = pre_generic_update_create_subsequence_builder
        self.__audience_age_controller = audience_age_controller
        self.__influencer_before_hooks = influencer_before_hooks
        self.__audience_age_after_hooks = audience_age_after_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_generic_update_create_subsequence_builder)\
            ._add_command(command=self.__influencer_before_hooks.validate_auth_influencer) \
            ._add_command(command=self.__audience_age_controller.update_for_influencer) \
            ._add_command(command=self.__audience_age_after_hooks.save_state)


class NotImplementedSequenceBuilder(FluentSequenceBuilder):

    def __init__(self):
        super().__init__()

    def build(self):
        self._add_command(lambda x: self.not_implemented(context=x))

    @staticmethod
    def not_implemented(context: PinfluencerContext):
        context.response.status_code = 501
        context.response.body = {"message": f"{context.route_key} route is not implemented"}