from mapper.object_mapper import ObjectMapper

from src.crosscutting import JsonCamelToSnakeCaseDeserializer, JsonSnakeToCamelSerializer
from src.data import SqlAlchemyDataManager
from src.data.repositories import SqlAlchemyBrandRepository, S3ImageRepository, SqlAlchemyInfluencerRepository, \
    CognitoAuthUserRepository, CognitoAuthService
from src.domain.validation import BrandValidator, InfluencerValidator
from src.types import DataManager, BrandRepository, BrandValidatable, Deserializer, ObjectMapperAdapter, \
    ImageRepository, Serializer, InfluencerRepository, AuthUserRepository
from src.web.controllers import BrandController, InfluencerController


class ServiceLocator:

    def get_new_data_manager(self) -> DataManager:
        return SqlAlchemyDataManager()

    def get_new_image_repository(self) -> ImageRepository:
        return S3ImageRepository()

    def get_new_brand_validator(self) -> BrandValidatable:
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
            brand_repository=self.get_new_brand_repository(),
            brand_validator=self.get_new_brand_validator(),
            deserializer=self.get_new_deserializer(),
            auth_user_repository=self.get_new_auth_user_repository())

    def get_new_influencer_controller(self) -> InfluencerController:
        return InfluencerController(influencer_repository=self.get_new_influencer_repository(),
                                    deserializer=self.get_new_deserializer(),
                                    auth_user_repository=self.get_new_auth_user_repository(),
                                    influencer_validator=self.get_new_influencer_validator())

    def get_new_serializer(self) -> Serializer:
        return JsonSnakeToCamelSerializer()

    def get_new_auth_user_repository(self) -> AuthUserRepository:
        return CognitoAuthUserRepository(auth_service=CognitoAuthService())

    def get_new_influencer_validator(self) -> InfluencerValidator:
        return InfluencerValidator()
