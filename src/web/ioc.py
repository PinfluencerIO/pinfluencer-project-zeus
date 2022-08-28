from mapper.object_mapper import ObjectMapper

from src.crosscutting import JsonCamelToSnakeCaseDeserializer, JsonSnakeToCamelSerializer
from src.data import SqlAlchemyDataManager
from src.data.repositories import S3ImageRepository, SqlAlchemyBrandRepository, SqlAlchemyInfluencerRepository, \
    CognitoAuthUserRepository, CognitoAuthService, SqlAlchemyCampaignRepository
from src.domain.validation import BrandValidator, InfluencerValidator, CampaignValidator
from src.types import DataManager, ImageRepository, ObjectMapperAdapter, BrandRepository, \
    InfluencerRepository, Deserializer, Serializer, AuthUserRepository, CampaignRepository
from src.web.controllers import BrandController, InfluencerController, CampaignController
from src.web.hooks import HooksFacade, CommonBeforeHooks, BrandAfterHooks, InfluencerAfterHooks, UserBeforeHooks, \
    UserAfterHooks, InfluencerBeforeHooks, BrandBeforeHooks, CampaignBeforeHooks, CampaignAfterHooks, CommonAfterHooks
from src.web.middleware import MiddlewarePipeline


class ServiceLocator:

    def get_new_data_manager(self) -> DataManager:
        return SqlAlchemyDataManager()

    def get_new_image_repository(self) -> ImageRepository:
        return S3ImageRepository()

    def get_new_brand_validator(self) -> BrandValidator:
        return BrandValidator()

    def get_new_object_mapper(self) -> ObjectMapperAdapter:
        return ObjectMapper()

    def get_new_brand_repository(self) -> BrandRepository:
        return SqlAlchemyBrandRepository(data_manager=self.get_new_data_manager(),
                                         image_repository=self.get_new_image_repository(),
                                         object_mapper=self.get_new_object_mapper())

    def get_new_influencer_repository(self) -> InfluencerRepository:
        return SqlAlchemyInfluencerRepository(data_manager=self.get_new_data_manager(),
                                              image_repository=self.get_new_image_repository(),
                                              object_mapper=self.get_new_object_mapper())

    def get_new_deserializer(self) -> Deserializer:
        return JsonCamelToSnakeCaseDeserializer()

    def get_new_brand_controller(self) -> BrandController:
        return BrandController(
            brand_repository=self.get_new_brand_repository())

    def get_new_influencer_controller(self) -> InfluencerController:
        return InfluencerController(influencer_repository=self.get_new_influencer_repository())

    def get_new_campaign_controller(self) -> CampaignController:
        return CampaignController(repository=self.get_new_campaign_repository())

    def get_new_serializer(self) -> Serializer:
        return JsonSnakeToCamelSerializer()

    def get_new_auth_user_repository(self) -> AuthUserRepository:
        return CognitoAuthUserRepository(auth_service=CognitoAuthService())

    def get_new_influencer_validator(self) -> InfluencerValidator:
        return InfluencerValidator()

    def get_new_middlware_pipeline(self) -> MiddlewarePipeline:
        return MiddlewarePipeline()

    def get_new_hooks_facade(self) -> HooksFacade:
        return HooksFacade(common_hooks=CommonBeforeHooks(deserializer=self.get_new_deserializer()),
                           brand_after_hooks=BrandAfterHooks(auth_user_repository=self.get_new_auth_user_repository()),
                           influencer_after_hooks=InfluencerAfterHooks(auth_user_repository=self.get_new_auth_user_repository()),
                           user_before_hooks=UserBeforeHooks(),
                           user_after_hooks=UserAfterHooks(auth_user_repository=self.get_new_auth_user_repository()),
                           influencer_before_hooks=InfluencerBeforeHooks(influencer_validator=self.get_new_influencer_validator()),
                           brand_before_hooks=BrandBeforeHooks(brand_validator=self.get_new_brand_validator(),
                                                               brand_repository=self.get_new_brand_repository()),
                           campaign_before_hooks=CampaignBeforeHooks(campaign_validator=CampaignValidator()),
                           campaign_after_hooks=CampaignAfterHooks(common_after_hooks=CommonAfterHooks()))

    def get_new_campaign_repository(self) -> CampaignRepository:
        return SqlAlchemyCampaignRepository(data_manager=self.get_new_data_manager(),
                                            object_mapper=self.get_new_object_mapper(),
                                            image_repository=self.get_new_image_repository())