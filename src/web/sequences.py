from src.web import FluentSequenceBuilder
from src.web.hooks import CommonBeforeHooks, CampaignBeforeHooks, CampaignAfterHooks, UserAfterHooks, UserBeforeHooks


class PreGenericUpdateCreateSubsequence(FluentSequenceBuilder):

    def __init__(self, common_before_hooks: CommonBeforeHooks,
                 user_before_hooks: UserBeforeHooks):
        super().__init__()
        self.__user_before_hooks = user_before_hooks
        self.__common_before_hooks = common_before_hooks

    def build(self):
        self.add_command(self.__common_before_hooks.set_body)\
            .add_command(self.__user_before_hooks.set_auth_user_id)


class PreUpdateCreateCampaignSubsequence(FluentSequenceBuilder):

    def __init__(self, campaign_before_hooks: CampaignBeforeHooks):
        super().__init__()
        self.__campaign_before_hooks = campaign_before_hooks

    def build(self):
        self.add_command(self.__campaign_before_hooks.map_campaign_state) \
            .add_command(self.__campaign_before_hooks.map_campaign_categories_and_values)


class PostSingleCampaignSubsequence(FluentSequenceBuilder):

    def __init__(self, campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
        self.__campaign_after_hooks = campaign_after_hooks

    def build(self):
        self.add_command(self.__campaign_after_hooks.format_campaign_state) \
            .add_command(self.__campaign_after_hooks.format_values_and_categories)


class PostMultipleCampaignSubsequence(FluentSequenceBuilder):

    def __init__(self, campaign_after_hooks: CampaignAfterHooks):
        super().__init__()
        self.__campaign_after_hooks = campaign_after_hooks

    def build(self):
        self.add_command(self.__campaign_after_hooks.format_campaign_state_collection) \
            .add_command(self.__campaign_after_hooks.format_values_and_categories_collection)


class PostSingleUserSubsequence(FluentSequenceBuilder):

    def __init__(self, user_after_hooks: UserAfterHooks):
        super().__init__()
        self.__user_after_hooks = user_after_hooks

    def build(self):
        self.add_command(self.__user_after_hooks.format_values_and_categories) \
            .add_command(self.__user_after_hooks.tag_auth_user_claims_to_response)


class PostMultipleUserSubsequence(FluentSequenceBuilder):

    def __init__(self, user_after_hooks: UserAfterHooks):
        super().__init__()
        self.__user_after_hooks = user_after_hooks

    def build(self):
        self.add_command(self.__user_after_hooks.format_values_and_categories_collection) \
            .add_command(self.__user_after_hooks.tag_auth_user_claims_to_response_collection)
