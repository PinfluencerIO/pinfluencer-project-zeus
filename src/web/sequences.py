from src.web import FluentSequenceBuilder, PinfluencerContext
from src.web.controllers import CampaignController
from src.web.hooks import CommonBeforeHooks, CampaignBeforeHooks, CampaignAfterHooks, UserAfterHooks, UserBeforeHooks, \
    BrandBeforeHooks, BrandAfterHooks


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
                 campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
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
            ._add_command(command=self.__campaign_controller.create) \
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
                 campaign_controller: CampaignController,
                 post_single_campaign_sequence: PostSingleCampaignSubsequenceBuilder,
                 campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
        self.__campaign_after_hooks = campaign_after_hooks
        self.__post_single_campaign_sequence = post_single_campaign_sequence
        self.__campaign_controller = campaign_controller
        self.__user_before_hooks = user_before_hooks

    def build(self):
        self._add_command(command=self.__user_before_hooks.set_auth_user_id)\
            ._add_command(command=self.__campaign_controller.get_for_brand) \
            ._add_sequence_builder(sequence_builder=self.__post_single_campaign_sequence) \
            ._add_command(command=self.__campaign_after_hooks.tag_bucket_url_to_images)


class NotImplementedSequenceBuilder(FluentSequenceBuilder):

    def __init__(self):
        super().__init__()

    def build(self):
        self._add_command(lambda x: self.not_implemented(context=x))

    @staticmethod
    def not_implemented(context: PinfluencerContext):
        context.response.status_code = 405
        context.response.body = {"message": "route is not implemented"}