from src.web import FluentSequenceBuilder, PinfluencerContext
from src.web.controllers import ListingController, InfluencerController, BrandController, NotificationController, \
    AudienceAgeController, AudienceGenderController, BrandListingController, CollaborationController, \
    InfluencerListingController
from src.web.hooks import CommonBeforeHooks, ListingBeforeHooks, ListingAfterHooks, UserAfterHooks, UserBeforeHooks, \
    BrandBeforeHooks, BrandAfterHooks, InfluencerBeforeHooks, InfluencerAfterHooks, NotificationBeforeHooks, \
    AudienceAgeBeforeHooks, CommonAfterHooks, AudienceAgeAfterHooks, AudienceGenderAfterHooks, \
    AudienceGenderBeforeHooks, InfluencerOnBoardingAfterHooks, CollaborationBeforeHooks, CollaborationAfterHooks


class PreGenericUpdateCreateSubsequenceBuilder(FluentSequenceBuilder):

    def __init__(self, common_before_hooks: CommonBeforeHooks,
                 user_before_hooks: UserBeforeHooks):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__common_before_hooks = common_before_hooks

    def build(self):
        self._add_command(self.__common_before_hooks.set_body)\
            ._add_command(self.__user_before_hooks.set_auth_user_id)


class PreUpdateCreateListingSubsequenceBuilder(FluentSequenceBuilder):

    def __init__(self, listing_before_hooks: ListingBeforeHooks):
        super().__init__()
        self.__listing_before_hooks = listing_before_hooks

    def build(self):
        self._add_command(self.__listing_before_hooks.map_categories_and_values)


class PostSingleUserSubsequenceBuilder(FluentSequenceBuilder):

    def __init__(self, user_after_hooks: UserAfterHooks):
        super().__init__()
        self.__user_after_hooks = user_after_hooks

    def build(self):
        self._add_command(self.__user_after_hooks.tag_auth_user_claims_to_response)


class PostMultipleUserSubsequenceBuilder(FluentSequenceBuilder):

    def __init__(self, user_after_hooks: UserAfterHooks):
        super().__init__()
        self.__user_after_hooks = user_after_hooks

    def build(self):
        self._add_command(self.__user_after_hooks.tag_auth_user_claims_to_response_collection)


class UpdateImageForListingSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 listing_before_hooks: ListingBeforeHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 listing_controller: ListingController,
                 generic_update_sequence: PreGenericUpdateCreateSubsequenceBuilder,
                 listing_after_hooks: ListingAfterHooks):
        super().__init__()
        self.__listing_after_hooks = listing_after_hooks
        self.__generic_update_sequence = generic_update_sequence
        self.__listing_controller = listing_controller
        self.__brand_before_hooks = brand_before_hooks
        self.__listing_before_hooks = listing_before_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__generic_update_sequence)\
            ._add_command(command=self.__listing_before_hooks.validate_id) \
            ._add_command(command=self.__brand_before_hooks.validate_auth_brand) \
            ._add_command(command=self.__listing_before_hooks.validate_image_key) \
            ._add_command(command=self.__listing_before_hooks.upload_image)\
            ._add_command(command=self.__listing_controller.update_listing_image) \
            ._add_command(command=self.__listing_after_hooks.tag_bucket_url_to_images)


class UpdateListingSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 listing_before_hooks: ListingBeforeHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 listing_controller: ListingController,
                 generic_update_sequence: PreGenericUpdateCreateSubsequenceBuilder,
                 listing_after_hooks: ListingAfterHooks):
        super().__init__()
        self.__listing_after_hooks = listing_after_hooks
        self.__generic_update_sequence = generic_update_sequence
        self.__brand_before_hooks = brand_before_hooks
        self.__listing_controller = listing_controller
        self.__listing_before_hooks = listing_before_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__generic_update_sequence)\
            ._add_command(command=self.__listing_before_hooks.validate_id)\
            ._add_command(command=self.__listing_before_hooks.validate_listing)\
            ._add_command(command=self.__brand_before_hooks.validate_auth_brand) \
            ._add_command(command=self.__listing_before_hooks.map_categories_and_values) \
            ._add_command(command=self.__listing_controller.update_listing)\
            ._add_command(command=self.__listing_after_hooks.tag_bucket_url_to_images)


class CreateListingSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 listing_before_hooks: ListingBeforeHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 listing_controller: ListingController,
                 generic_update_sequence: PreGenericUpdateCreateSubsequenceBuilder,
                 common_after_hooks: CommonAfterHooks,
                 listing_after_hooks: ListingAfterHooks):
        super().__init__()
        self.__common_after_hooks = common_after_hooks
        self.__listing_after_hooks = listing_after_hooks
        self.__generic_update_sequence = generic_update_sequence
        self.__brand_before_hooks = brand_before_hooks
        self.__listing_controller = listing_controller
        self.__listing_before_hooks = listing_before_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__generic_update_sequence) \
            ._add_command(command=self.__listing_before_hooks.validate_listing) \
            ._add_command(command=self.__brand_before_hooks.validate_auth_brand) \
            ._add_command(command=self.__listing_before_hooks.map_categories_and_values) \
            ._add_command(command=self.__listing_controller.create_for_brand) \
            ._add_command(command=self.__listing_after_hooks.save_state) \
            ._add_command(command=self.__listing_after_hooks.tag_bucket_url_to_images)


class GetListingByIdSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 listing_before_hooks: ListingBeforeHooks,
                 listing_controller: ListingController,
                 listing_after_hooks: ListingAfterHooks):
        super().__init__()
        self.__listing_after_hooks = listing_after_hooks
        self.__listing_controller = listing_controller
        self.__listing_before_hooks = listing_before_hooks

    def build(self):
        self._add_command(command=self.__listing_before_hooks.validate_id) \
            ._add_command(command=self.__listing_controller.get_by_id)\
            ._add_command(command=self.__listing_after_hooks.tag_bucket_url_to_images)


class GetListingsForBrandSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 user_before_hooks: UserBeforeHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 listing_controller: ListingController,
                 listing_after_hooks: ListingAfterHooks):
        super().__init__()
        self.__brand_before_hooks = brand_before_hooks
        self.__listing_after_hooks = listing_after_hooks
        self.__listing_controller = listing_controller
        self.__user_before_hooks = user_before_hooks

    def build(self):
        self._add_command(command=self.__user_before_hooks.set_auth_user_id) \
            ._add_command(command=self.__brand_before_hooks.validate_auth_brand) \
            ._add_command(command=self.__listing_controller.get_for_brand) \
            ._add_command(command=self.__listing_after_hooks.tag_bucket_url_to_images_collection)


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


class GetAudienceGenderSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, audience_gender_controller: AudienceGenderController,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 user_before_hooks: UserBeforeHooks):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__influencer_before_hooks = influencer_before_hooks
        self.__audience_gender_controller = audience_gender_controller

    def build(self):
        self._add_command(command=self.__user_before_hooks.set_auth_user_id)\
            ._add_command(command=self.__influencer_before_hooks.validate_auth_influencer)\
            ._add_command(command=self.__audience_gender_controller.get_for_influencer)


class UpdateAudienceGenderSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 audience_gender_controller: AudienceGenderController,
                 pre_generic_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 audience_gender_after_hooks: AudienceGenderAfterHooks,
                 audience_gender_before_hooks: AudienceGenderBeforeHooks):
        super().__init__()
        self.__pre_generic_update_create_subsequence_builder = pre_generic_update_create_subsequence_builder
        self.__audience_gender_controller = audience_gender_controller
        self.__influencer_before_hooks = influencer_before_hooks
        self.__audience_gender_after_hooks = audience_gender_after_hooks
        self.__audience_gender_before_hooks = audience_gender_before_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_generic_update_create_subsequence_builder)\
            ._add_command(command=self.__influencer_before_hooks.validate_auth_influencer)\
            ._add_command(command=self.__audience_gender_controller.update_for_influencer)\
            ._add_command(command=self.__audience_gender_after_hooks.save_state)


class CreateInfluencerProfileSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 post_user_single_sequence_builder: PostSingleUserSubsequenceBuilder,
                 influencer_controller: InfluencerController,
                 influencer_after_hooks: InfluencerAfterHooks,
                 influencer_onboarding_hooks: InfluencerOnBoardingAfterHooks,
                 user_before_hooks: UserBeforeHooks,
                 audience_age_controller: AudienceAgeController,
                 audience_age_before_hooks: AudienceAgeBeforeHooks,
                 audience_gender_controller: AudienceGenderController,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 audience_gender_before_hooks: AudienceGenderBeforeHooks,
                 pre_generic_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder):
        super().__init__()
        self.__post_user_single_sequence_builder = post_user_single_sequence_builder
        self.__influencer_controller = influencer_controller
        self.__influencer_after_hooks = influencer_after_hooks
        self.__user_before_hooks = user_before_hooks
        self.__audience_age_controller = audience_age_controller
        self.__audience_age_before_hooks = audience_age_before_hooks
        self.__audience_gender_controller = audience_gender_controller
        self.__influencer_before_hooks = influencer_before_hooks
        self.__audience_gender_before_hooks = audience_gender_before_hooks
        self.__pre_generic_update_create_subsequence_builder = pre_generic_update_create_subsequence_builder
        self.__influencer_onboarding_hooks = influencer_onboarding_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_generic_update_create_subsequence_builder) \
            ._add_command(command=self.__audience_gender_before_hooks.check_audience_genders_are_empty) \
            ._add_command(command=self.__audience_gender_controller.create_for_influencer) \
            ._add_command(command=self.__influencer_onboarding_hooks.cache_audience_gender_data) \
            ._add_command(command=self.__audience_age_before_hooks.check_audience_ages_are_empty) \
            ._add_command(command=self.__audience_age_controller.create_for_influencer) \
            ._add_command(command=self.__influencer_onboarding_hooks.cache_audience_age_data) \
            ._add_command(command=self.__user_before_hooks.set_categories_and_values) \
            ._add_command(command=self.__influencer_controller.create) \
            ._add_command(command=self.__influencer_onboarding_hooks.cache_influencer_data) \
            ._add_command(command=self.__influencer_onboarding_hooks.merge_influencer_cache) \
            ._add_command(command=self.__influencer_after_hooks.set_influencer_claims) \
            ._add_sequence_builder(sequence_builder=self.__post_user_single_sequence_builder) \
            ._add_command(command=self.__influencer_after_hooks.tag_bucket_url_to_images)


class UpdateInfluencerProfileSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 influencer_onboarding_hooks: InfluencerOnBoardingAfterHooks,
                 pre_generic_update_create_subsequence_builder: PreGenericUpdateCreateSubsequenceBuilder,
                 audience_gender_controller: AudienceGenderController,
                 audience_age_controller: AudienceAgeController,
                 user_before_hooks: UserBeforeHooks,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 influencer_controller: InfluencerController,
                 influencer_after_hooks: InfluencerAfterHooks,
                 post_user_single_sequence_builder: PostSingleUserSubsequenceBuilder):
        super().__init__()
        self.__post_user_single_sequence_builder = post_user_single_sequence_builder
        self.__influencer_after_hooks = influencer_after_hooks
        self.__influencer_controller = influencer_controller
        self.__influencer_before_hooks = influencer_before_hooks
        self.__user_before_hooks = user_before_hooks
        self.__audience_age_controller = audience_age_controller
        self.__audience_gender_controller = audience_gender_controller
        self.__pre_generic_update_create_subsequence_builder = pre_generic_update_create_subsequence_builder
        self.__influencer_onboarding_hooks = influencer_onboarding_hooks

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__pre_generic_update_create_subsequence_builder)\
            ._add_command(command=self.__audience_gender_controller.update_for_influencer) \
            ._add_command(command=self.__influencer_onboarding_hooks.cache_audience_gender_data) \
            ._add_command(command=self.__audience_age_controller.update_for_influencer) \
            ._add_command(command=self.__influencer_onboarding_hooks.cache_audience_age_data) \
            ._add_command(command=self.__user_before_hooks.set_categories_and_values) \
            ._add_command(command=self.__influencer_before_hooks.validate_influencer) \
            ._add_command(command=self.__influencer_controller.update_for_user) \
            ._add_command(command=self.__influencer_onboarding_hooks.cache_influencer_data) \
            ._add_command(command=self.__influencer_onboarding_hooks.merge_influencer_cache) \
            ._add_command(command=self.__influencer_after_hooks.set_influencer_claims) \
            ._add_sequence_builder(sequence_builder=self.__post_user_single_sequence_builder)


class GetInfluencerProfileSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 influencer_onboarding_hooks: InfluencerOnBoardingAfterHooks,
                 user_before_hooks: UserBeforeHooks,
                 audience_gender_controller: AudienceGenderController,
                 audience_age_controller: AudienceAgeController,
                 influencer_controller: InfluencerController,
                 post_user_single_sequence_builder: PostSingleUserSubsequenceBuilder,
                 influencer_after_hooks: InfluencerAfterHooks):
        super().__init__()
        self.__influencer_after_hooks = influencer_after_hooks
        self.__post_user_single_sequence_builder = post_user_single_sequence_builder
        self.__influencer_controller = influencer_controller
        self.__audience_age_controller = audience_age_controller
        self.__audience_gender_controller = audience_gender_controller
        self.__user_before_hooks = user_before_hooks
        self.__influencer_onboarding_hooks = influencer_onboarding_hooks

    def build(self):
        self._add_command(command=self.__user_before_hooks.set_auth_user_id) \
            ._add_command(command=self.__audience_gender_controller.get_for_influencer) \
            ._add_command(command=self.__influencer_onboarding_hooks.cache_audience_gender_data) \
            ._add_command(command=self.__audience_age_controller.get_for_influencer) \
            ._add_command(command=self.__influencer_onboarding_hooks.cache_audience_age_data) \
            ._add_command(command=self.__influencer_controller.get) \
            ._add_command(command=self.__influencer_onboarding_hooks.cache_influencer_data) \
            ._add_command(command=self.__influencer_onboarding_hooks.merge_influencer_cache) \
            ._add_sequence_builder(sequence_builder=self.__post_user_single_sequence_builder)


class GetBrandListingsForBrandSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 user_before_hooks: UserBeforeHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 brand_listing_controller: BrandListingController,
                 listing_after_hooks: ListingAfterHooks):
        super().__init__()
        self.__brand_before_hooks = brand_before_hooks
        self.__listing_after_hooks = listing_after_hooks
        self.__brand_listing_controller = brand_listing_controller
        self.__user_before_hooks = user_before_hooks

    def build(self):
        self._add_command(command=self.__user_before_hooks.set_auth_user_id)\
            ._add_command(command=self.__brand_before_hooks.validate_brand)\
            ._add_command(command=self.__brand_listing_controller.get_for_brand)\
            ._add_command(command=self.__listing_after_hooks.tag_bucket_url_to_images_collection)


class CreateCollaborationForInfluencerSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 common_before_hooks: CommonBeforeHooks,
                 user_before_hooks: UserBeforeHooks,
                 collaboration_before_hooks: CollaborationBeforeHooks,
                 collaboration_controller: CollaborationController,
                 collaboration_after_hooks: CollaborationAfterHooks):
        super().__init__()
        self.__collaboration_after_hooks = collaboration_after_hooks
        self.__collaboration_before_hooks = collaboration_before_hooks
        self.__user_before_hooks = user_before_hooks
        self.__collaboration_controller = collaboration_controller
        self.__common_before_hooks = common_before_hooks

    def build(self):
        self._add_command(command=self.__common_before_hooks.set_body)\
            ._add_command(command=self.__user_before_hooks.set_auth_user_id) \
            ._add_command(command=self.__collaboration_before_hooks.load_brand_from_listing_to_request_body)\
            ._add_command(command=self.__collaboration_controller.create_for_influencer) \
            ._add_command(command=self.__collaboration_after_hooks.save_state)


class GetListingsForInfluencerSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 influencer_listing_controller: InfluencerListingController):
        super().__init__()
        self.__influencer_listing_controller = influencer_listing_controller

    def build(self):
        self._add_command(command=self.__influencer_listing_controller.get_all)


class SequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 influencer_listing_controller: InfluencerListingController):
        super().__init__()
        self.__influencer_listing_controller = influencer_listing_controller

    def build(self):
        self._add_command(command=self.__influencer_listing_controller.get_all)


class NotImplementedSequenceBuilder(FluentSequenceBuilder):

    def __init__(self):
        super().__init__()

    def build(self):
        self._add_command(lambda x: self.not_implemented(context=x))

    @staticmethod
    def not_implemented(context: PinfluencerContext):
        context.response.status_code = 501
        context.response.body = {"message": f"{context.route_key} route is not implemented"}