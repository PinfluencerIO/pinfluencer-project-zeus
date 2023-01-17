from typing import Any, Callable

from jsonschema.exceptions import ValidationError

from src._types import AuthUserRepository, Deserializer, BrandRepository, ImageRepository, Logger, \
    NotificationRepository, AudienceAgeRepository, InfluencerRepository, ListingRepository, Repository, \
    AudienceGenderRepository
from src.crosscutting import PinfluencerObjectMapper
from src.domain.models import CategoryEnum, ValueEnum, User
from src.domain.validation import BrandValidator, InfluencerValidator, ListingValidator
from src.exceptions import NotFoundException
from src.web import PinfluencerContext, valid_path_resource_id, ErrorCapsule
from src.web.constants import AudienceAgeCacheKey, InfluencerDetailsCacheKey, AudienceGenderCacheKey
from src.web.error_capsules import AudienceDataAlreadyExistsErrorCapsule, BrandNotFoundErrorCapsule, \
    InfluencerNotFoundErrorCapsule, ListingNotFoundErrorCapsule
from src.web.views import RawImageRequestDto, ImageRequestDto, ListingResponseDto, NotificationCreateRequestDto

S3_URL = "https://pinfluencer-product-images.s3.eu-west-2.amazonaws.com"


class CommonAfterHooks:

    def set_image_url(self,
                      context: PinfluencerContext,
                      image_fields: list[str],
                      collection: bool = False):
        if collection:
            for entity in context.response.body:
                self.__set_image_fields(entity=entity, fields=image_fields)
        else:
            self.__set_image_fields(entity=context.response.body, fields=image_fields)

    def __set_image_fields(self, entity: dict, fields: list[str]):
        for field in fields:
            self.__set_image(entity=entity, field=field)

    def __set_image(self, entity: dict, field: str):
        if entity[field] is not None:
            entity[field] = f'{S3_URL}/{entity[field]}'

    def save_response_body_to_cache(self,
                                    context: PinfluencerContext,
                                    key: str):
        context.cached_values[key] = context.response.body

    def merge_cached_values_to_response(self,
                                        context: PinfluencerContext,
                                        keys: list[str]):
        merged_body = {}
        for key in keys:
            merged_body.update(context.cached_values[key])
        context.response.body = merged_body


class CommonBeforeHooks:

    def __init__(self, deserializer: Deserializer,
                 image_repo: ImageRepository,
                 object_mapper: PinfluencerObjectMapper,
                 logger: Logger):
        self.__logger = logger
        self.__object_mapper = object_mapper
        self.__image_repo = image_repo
        self.__deserializer = deserializer

    def validate_image_path(self, context: PinfluencerContext,
                            possible_paths: list[str]):
        if not possible_paths.__contains__(context.event['pathParameters']["image_field"]):
            context.response.status_code = 400
            context.response.body = {}
            context.short_circuit = True
            self.__logger.log_error(f"{context.event['pathParameters']['image_field']} is not a valid image field")

    def upload_image(self, context: PinfluencerContext,
                     path: str,
                     map_list: dict):
        request: RawImageRequestDto = self.__object_mapper.map_from_dict(_from=context.body, to=RawImageRequestDto)
        key = self.__image_repo.upload(path=path, image_base64_encoded=request.image_bytes)
        context.body = ImageRequestDto(image_path=key,
                                       image_field=map_list[context.event['pathParameters']['image_field']]).__dict__

    def map_enum(self, context: PinfluencerContext,
                 key: str,
                 enum_value):
        if key in context.body:
            context.body[key] = enum_value[context.body[key]]

    def map_enums(self, context: PinfluencerContext,
                  key: str,
                  enum_value):
        if key in context.body:
            context.body[key] = list(map(lambda x: enum_value[x], context.body[key]))

    def set_body(self, context: PinfluencerContext):
        context.body = self.__deserializer.deserialize(data=context.event["body"])


class ListingBeforeHooks:

    def __init__(self, listing_validator: ListingValidator,
                 common_before_hooks: CommonBeforeHooks,
                 logger: Logger):
        self.__logger = logger
        self.__common_before_hooks = common_before_hooks
        self.__listing_validator = listing_validator

    def map_categories_and_values(self, context: PinfluencerContext):
        self.__common_before_hooks.map_enums(context=context,
                                             key="categories",
                                             enum_value=CategoryEnum)
        self.__common_before_hooks.map_enums(context=context,
                                             key="values",
                                             enum_value=ValueEnum)

    def validate_listing(self, context: PinfluencerContext):
        try:
            self.__listing_validator.validate_listing(payload=context.body)
        except ValidationError as e:
            self.__logger.log_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400

    def validate_id(self, context: PinfluencerContext):
        id = valid_path_resource_id(event=context.event, resource_key="listing_id", logger=self.__logger)
        if not id:
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400
        else:
            context.id = id

    def upload_image(self, context: PinfluencerContext):
        self.__common_before_hooks.upload_image(path=f"listings/{context.auth_user_id}", context=context, map_list={
            "product-image": "product_image"
        })

    def validate_image_key(self, context: PinfluencerContext):
        self.__common_before_hooks.validate_image_path(context=context, possible_paths=["product-image"])


class SaveableHook:
    def __init__(self, repository: Repository):
        self.__repository = repository

    def save_state(self, context: PinfluencerContext):
        self.__repository.save()


class ListingAfterHooks(SaveableHook):

    def __init__(self, common_after_hooks: CommonAfterHooks, mapper: PinfluencerObjectMapper,
                 repository: ListingRepository):
        super().__init__(repository)
        self.__mapper = mapper
        self.__common_after_hooks = common_after_hooks

    def tag_bucket_url_to_images(self, context: PinfluencerContext):
        self.__common_after_hooks.set_image_url(context=context,
                                                image_fields=["product_image"],
                                                collection=False)

    def tag_bucket_url_to_images_collection(self, context: PinfluencerContext):
        self.__common_after_hooks.set_image_url(context=context,
                                                image_fields=["product_image"],
                                                collection=True)

    def validate_listing_belongs_to_brand(self, context: PinfluencerContext):
        brand_response: ListingResponseDto = self.__mapper.map_from_dict(_from=context.response.body, to=ListingResponseDto)
        if not (brand_response.brand_auth_user_id == context.auth_user_id):
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 403


class BrandAfterHooks:

    def __init__(self, auth_user_repository: AuthUserRepository,
                 common_after_common_hooks: CommonAfterHooks,
                 mapper: PinfluencerObjectMapper):
        self.__mapper = mapper
        self.__common_after_common_hooks = common_after_common_hooks
        self.__auth_user_repository = auth_user_repository

    def set_brand_claims(self, context: PinfluencerContext):
        user: User = self.__mapper.map_from_dict(_from=context.body, to=User)
        self.__auth_user_repository.update_brand_claims(user=user, auth_user_id=context.auth_user_id)

    def tag_bucket_url_to_images(self, context: PinfluencerContext):
        self.__common_after_common_hooks.set_image_url(context=context,
                                                       image_fields=["header_image",
                                                                     "logo"],
                                                       collection=False)

    def tag_bucket_url_to_images_collection(self, context: PinfluencerContext):
        self.__common_after_common_hooks.set_image_url(context=context,
                                                       image_fields=["header_image",
                                                                     "logo"],
                                                       collection=True)


class InfluencerAfterHooks:

    def __init__(self, auth_user_repository: AuthUserRepository,
                 common_after_hooks: CommonAfterHooks,
                 mapper: PinfluencerObjectMapper):
        self.__mapper = mapper
        self.__common_after_hooks = common_after_hooks
        self.__auth_user_repository = auth_user_repository

    def set_influencer_claims(self, context: PinfluencerContext):
        user: User = self.__mapper.map_from_dict(_from=context.body, to=User)
        self.__auth_user_repository.update_influencer_claims(user=user,
                                                             auth_user_id=context.auth_user_id)

    def tag_bucket_url_to_images(self, context: PinfluencerContext):
        self.__common_after_hooks.set_image_url(context=context,
                                                image_fields=["image"],
                                                collection=False)

    def tag_bucket_url_to_images_collection(self, context: PinfluencerContext):
        self.__common_after_hooks.set_image_url(context=context,
                                                image_fields=["image"],
                                                collection=True)


class CollaborationBeforeHooks:

    def __init__(self, listings_repository: ListingRepository):
        self.__listings_repository = listings_repository

    def load_brand_from_listing_to_request_body(self, context: PinfluencerContext):
        try:
            context.body["brand_auth_user_id"] = self.__listings_repository.load_by_id(id_=context.body["listing_id"]).brand_auth_user_id
        except NotFoundException:
            context.error_capsule = [ListingNotFoundErrorCapsule(id=context.body["listing_id"])]


class UserBeforeHooks:

    def __init__(self, common_before_hooks: CommonBeforeHooks,
                 logger: Logger):
        self.__logger = logger
        self.__common_before_hooks = common_before_hooks

    def set_auth_user_id(self, context: PinfluencerContext):
        context.auth_user_id = context.event['requestContext']['authorizer']['jwt']['claims']['username']
        self.__logger.log_trace(f"username {context.auth_user_id}")

    def set_categories_and_values(self, context: PinfluencerContext):
        self.__common_before_hooks.map_enums(context=context,
                                             key="values",
                                             enum_value=ValueEnum)
        self.__common_before_hooks.map_enums(context=context,
                                             key="categories",
                                             enum_value=CategoryEnum)

    def validate_owner(self, context: PinfluencerContext,
                       repo_method: Callable[[str], Any],
                       capsule: ErrorCapsule):
        try:
            repo_method(context.auth_user_id)
        except NotFoundException as e:
            self.__logger.log_exception(e)
            context.error_capsule.append(capsule)


class InfluencerBeforeHooks:

    def __init__(self, influencer_validator: InfluencerValidator,
                 common_before_hooks: CommonBeforeHooks,
                 logger: Logger,
                 influencer_repository: InfluencerRepository,
                 user_before_hooks: UserBeforeHooks):
        self.__logger = logger
        self.__common_before_hooks = common_before_hooks
        self.__influencer_validator = influencer_validator
        self.__influencer_repository = influencer_repository
        self.__user_before_hooks = user_before_hooks

    def validate_uuid(self, context: PinfluencerContext):
        id = valid_path_resource_id(event=context.event, resource_key="influencer_id", logger=self.__logger)
        if not id:
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400
        else:
            context.id = id

    def validate_influencer(self, context: PinfluencerContext):
        try:
            self.__influencer_validator.validate_influencer(payload=context.body)
        except ValidationError as e:
            self.__logger.log_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400

    def upload_image(self, context: PinfluencerContext):
        self.__common_before_hooks.upload_image(path=f"influencers/{context.auth_user_id}", context=context, map_list={
            "image": "image"
        })

    def validate_image_key(self, context: PinfluencerContext):
        self.__common_before_hooks.validate_image_path(context=context, possible_paths=["image"])

    def validate_auth_influencer(self, context: PinfluencerContext):
        self.__user_before_hooks.validate_owner(context=context,
                                                repo_method=self.__influencer_repository.load_for_auth_user,
                                                capsule=InfluencerNotFoundErrorCapsule(auth_user_id=context.auth_user_id))


class BrandBeforeHooks:

    def __init__(self, brand_validator: BrandValidator,
                 brand_repository: BrandRepository,
                 common_before_hooks: CommonBeforeHooks,
                 user_before_hooks: UserBeforeHooks,
                 logger: Logger):
        self.__user_before_hooks = user_before_hooks
        self.__logger = logger
        self.__common_before_hooks = common_before_hooks
        self.__brand_repository = brand_repository
        self.__brand_validator = brand_validator

    def validate_auth_brand(self, context: PinfluencerContext):
        self.__user_before_hooks.validate_owner(context=context,
                                                repo_method=self.__brand_repository.load_for_auth_user,
                                                capsule=BrandNotFoundErrorCapsule(auth_user_id=context.auth_user_id))


    def validate_uuid(self, context: PinfluencerContext):
        id = valid_path_resource_id(event=context.event, resource_key="brand_id", logger=self.__logger)
        if not id:
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400
        else:
            context.id = id

    def validate_brand(self, context: PinfluencerContext):
        try:
            self.__brand_validator.validate_brand(payload=context.body)
        except ValidationError as e:
            self.__logger.log_exception(e)
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400

    def upload_image(self, context: PinfluencerContext):
        self.__common_before_hooks.upload_image(path=f"brands/{context.auth_user_id}", context=context, map_list={
            "logo": "logo",
            "header-image": "header_image"
        })

    def validate_image_key(self, context: PinfluencerContext):
        self.__common_before_hooks.validate_image_path(context=context, possible_paths=["logo", "header-image"])


class UserAfterHooks:

    def __init__(self, auth_user_repository: AuthUserRepository,
                 common_after_hooks: CommonAfterHooks,
                 mapper: PinfluencerObjectMapper):
        self.__mapper = mapper
        self.__common_after_hooks = common_after_hooks
        self.__auth_user_repository = auth_user_repository

    def tag_auth_user_claims_to_response(self, context: PinfluencerContext):
        self._generic_claims_tagger(context.response.body)

    def _generic_claims_tagger(self, entity):
        auth_user = self.__auth_user_repository.get_by_id(_id=entity["auth_user_id"])
        entity.update(auth_user.__dict__)

    def tag_auth_user_claims_to_response_collection(self, context: PinfluencerContext):
        for user in context.response.body:
            self._generic_claims_tagger(entity=user)


class HooksFacade:

    def __init__(self, common_hooks: CommonBeforeHooks,
                 brand_after_hooks: BrandAfterHooks,
                 influencer_after_hooks: InfluencerAfterHooks,
                 user_before_hooks: UserBeforeHooks,
                 user_after_hooks: UserAfterHooks,
                 influencer_before_hooks: InfluencerBeforeHooks,
                 brand_before_hooks: BrandBeforeHooks,
                 listing_before_hooks: ListingBeforeHooks,
                 listing_after_hooks: ListingAfterHooks):
        self.__listing_before_hooks = listing_before_hooks
        self.__brand_before_hooks = brand_before_hooks
        self.__influencer_before_hooks = influencer_before_hooks
        self.__user_after_hooks = user_after_hooks
        self.__influencer_after_hooks = influencer_after_hooks
        self.__user_before_hooks = user_before_hooks
        self.__brand_after_hooks = brand_after_hooks
        self.__common_before_hooks = common_hooks
        self.__listing_after_hooks = listing_after_hooks

    def get_listing_after_hooks(self) -> ListingAfterHooks:
        return self.__listing_after_hooks

    def get_listing_before_hooks(self) -> ListingBeforeHooks:
        return self.__listing_before_hooks

    def get_brand_before_hooks(self) -> BrandBeforeHooks:
        return self.__brand_before_hooks

    def get_influencer_before_hooks(self) -> InfluencerBeforeHooks:
        return self.__influencer_before_hooks

    def get_user_after_hooks(self) -> UserAfterHooks:
        return self.__user_after_hooks

    def get_influencer_after_hooks(self) -> InfluencerAfterHooks:
        return self.__influencer_after_hooks

    def get_user_before_hooks(self) -> UserBeforeHooks:
        return self.__user_before_hooks

    def get_brand_after_hooks(self) -> BrandAfterHooks:
        return self.__brand_after_hooks

    def get_before_common_hooks(self) -> CommonBeforeHooks:
        return self.__common_before_hooks


class NotificationBeforeHooks:

    def __init__(self, mapper: PinfluencerObjectMapper,
                 logger: Logger):
        self.__logger = logger
        self.__mapper = mapper

    def override_create_fields(self, context: PinfluencerContext):
        notification = self.__mapper.map_from_dict(_from=context.body, to=NotificationCreateRequestDto)
        notification.sender_auth_user_id = context.auth_user_id
        notification.read = False
        context.body = notification.__dict__

    def validate_uuid(self, context: PinfluencerContext):
        id = valid_path_resource_id(event=context.event, resource_key="notification_id", logger=self.__logger)
        if not id:
            context.short_circuit = True
            context.response.body = {}
            context.response.status_code = 400
        else:
            context.id = id


class NotificationAfterHooks(SaveableHook):

    def __init__(self, repository: NotificationRepository):
        super().__init__(repository)


class AudienceCommonHooks:

    def check_audience_data_is_empty(self, context: PinfluencerContext,
                                     repo_method: Callable[[str], Any],
                                     audience_splits_getter: Callable[[Any], list[Any]]):
        audience_split = repo_method(context.auth_user_id)
        if audience_splits_getter(audience_split) != []:
            context.error_capsule.append(AudienceDataAlreadyExistsErrorCapsule(auth_user_id=context.auth_user_id))


class AudienceAgeAfterHooks(SaveableHook):

    def __init__(self, repository: AudienceAgeRepository):
        super().__init__(repository)


class AudienceGenderAfterHooks(SaveableHook):

    def __init__(self, repository: AudienceGenderRepository):
        super().__init__(repository)


class AudienceAgeBeforeHooks:

    def __init__(self, repository: AudienceAgeRepository,
                 audience_age_common_hooks: AudienceCommonHooks):
        self.__audience_age_common_hooks = audience_age_common_hooks
        self.__repository = repository

    def check_audience_ages_are_empty(self, context: PinfluencerContext):
        self.__audience_age_common_hooks.check_audience_data_is_empty(context=context,
                                                                      repo_method=self.__repository.load_for_influencer,
                                                                      audience_splits_getter=lambda x: x.audience_ages)


class AudienceGenderBeforeHooks:

    def __init__(self, repository: AudienceGenderRepository,
                 audience_common_hooks: AudienceCommonHooks):
        self.__audience_age_common_hooks = audience_common_hooks
        self.__repository = repository

    def check_audience_genders_are_empty(self, context: PinfluencerContext):
        self.__audience_age_common_hooks.check_audience_data_is_empty(context=context,
                                                                      repo_method=self.__repository.load_for_influencer,
                                                                      audience_splits_getter=lambda x: x.audience_genders)


class InfluencerOnBoardingAfterHooks:

    def __init__(self, common_after_hooks: CommonAfterHooks):
        self.__common_after_hooks = common_after_hooks

    def cache_audience_age_data(self, context: PinfluencerContext):
        self.__common_after_hooks.save_response_body_to_cache(context=context,
                                                              key=AudienceAgeCacheKey)

    def merge_influencer_cache(self, context: PinfluencerContext):
        self.__common_after_hooks.merge_cached_values_to_response(context=context,
                                                                  keys=[
                                                                      InfluencerDetailsCacheKey,
                                                                      AudienceAgeCacheKey,
                                                                      AudienceGenderCacheKey
                                                                  ])

    def cache_influencer_data(self, context: PinfluencerContext):
        self.__common_after_hooks.save_response_body_to_cache(context=context,
                                                              key=InfluencerDetailsCacheKey)

    def cache_audience_gender_data(self, context: PinfluencerContext):
        self.__common_after_hooks.save_response_body_to_cache(context=context,
                                                              key=AudienceGenderCacheKey)