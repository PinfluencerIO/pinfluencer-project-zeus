import os

from simple_injection import ServiceCollection

from src import ServiceLocator
from src._types import DataManager, BrandRepository, InfluencerRepository, ListingRepository, ImageRepository, \
    Deserializer, Serializer, AuthUserRepository, Logger, NotificationRepository, AudienceAgeRepository, \
    AudienceGenderRepository, BrandListingRepository, CollaborationRepository, InfluencerListingRepository
from src.crosscutting import JsonCamelToSnakeCaseDeserializer, JsonSnakeToCamelSerializer, \
    PinfluencerObjectMapper, FlexiUpdater, ConsoleLogger, DummyLogger
from src.data import SqlAlchemyDataManager
from src.data.repositories import SqlAlchemyBrandRepository, SqlAlchemyInfluencerRepository, \
    SqlAlchemyListingRepository, S3ImageRepository, CognitoAuthUserRepository, CognitoAuthService, \
    SqlAlchemyNotificationRepository, SqlAlchemyAudienceAgeRepository, SqlAlchemyAudienceGenderRepository, \
    SqlAlchemyBrandListingRepository, SqlAlchemyCollaborationRepository, SqlAlchemyInfluencerListingRepository
from src.domain.validation import BrandValidator, ListingValidator, InfluencerValidator
from src.web import PinfluencerResponse, PinfluencerContext, Route
from src.web.controllers import BrandController, InfluencerController, ListingController, NotificationController, \
    AudienceAgeController, AudienceGenderController, BrandListingController, CollaborationController, \
    InfluencerListingController
from src.web.hooks import HooksFacade, CommonBeforeHooks, BrandAfterHooks, InfluencerAfterHooks, UserBeforeHooks, \
    UserAfterHooks, InfluencerBeforeHooks, BrandBeforeHooks, ListingBeforeHooks, ListingAfterHooks, CommonAfterHooks, \
    NotificationAfterHooks, NotificationBeforeHooks, AudienceAgeBeforeHooks, AudienceCommonHooks, \
    AudienceAgeAfterHooks, AudienceGenderAfterHooks, AudienceGenderBeforeHooks, InfluencerOnBoardingAfterHooks, \
    CollaborationBeforeHooks, CollaborationAfterHooks
from src.web.mapping import MappingRules
from src.web.middleware import MiddlewarePipeline
from src.web.routing import Dispatcher
from src.web.sequences import PreGenericUpdateCreateSubsequenceBuilder, PreUpdateCreateListingSubsequenceBuilder, \
    PostSingleUserSubsequenceBuilder, \
    PostMultipleUserSubsequenceBuilder, UpdateImageForListingSequenceBuilder, NotImplementedSequenceBuilder, \
    UpdateListingSequenceBuilder, CreateListingSequenceBuilder, GetListingByIdSequenceBuilder, \
    GetListingsForBrandSequenceBuilder, UpdateInfluencerImageSequenceBuilder, UpdateInfluencerSequenceBuilder, \
    CreateInfluencerSequenceBuilder, GetAuthInfluencerSequenceBuilder, GetInfluencerByIdSequenceBuilder, \
    GetAllInfluencersSequenceBuilder, UpdateBrandImageSequenceBuilder, UpdateBrandSequenceBuilder, \
    CreateBrandSequenceBuilder, GetAuthBrandSequenceBuilder, GetBrandByIdSequenceBuilder, GetAllBrandsSequenceBuilder, \
    CreateNotificationSequenceBuilder, GetNotificationByIdSequenceBuilder, CreateAudienceAgeSequenceBuilder, \
    GetAudienceAgeSequenceBuilder, UpdateAudienceAgeSequenceBuilder, CreateAudienceGenderSequenceBuilder, \
    GetAudienceGenderSequenceBuilder, UpdateAudienceGenderSequenceBuilder, CreateInfluencerProfileSequenceBuilder, \
    UpdateInfluencerProfileSequenceBuilder, GetInfluencerProfileSequenceBuilder, \
    GetBrandListingsForBrandSequenceBuilder, CreateCollaborationForInfluencerSequenceBuilder, \
    GetListingsForInfluencerSequenceBuilder


def lambda_handler(event, context):
    return bootstrap(event=event,
                     context=context,

                     # infra for testability
                     middleware=MiddlewarePipeline(logger=logger_factory()),
                     ioc=ServiceCollection(),
                     data_manager=SqlAlchemyDataManager(logger=logger_factory()),
                     cognito_auth_service=CognitoAuthService(logger=logger_factory()))


def logger_factory():
    if "ENVIRONMENT" in os.environ:
        if os.environ["ENVIRONMENT"] == "TEST":
            return DummyLogger()
    return ConsoleLogger()


def bootstrap(event: dict,
              context: dict,
              middleware: MiddlewarePipeline,
              ioc: ServiceCollection,
              data_manager: DataManager,
              cognito_auth_service: CognitoAuthService) -> dict:
    try:
        register_dependencies(cognito_auth_service,
                              data_manager,
                              ioc,
                              middleware)

        # register custom mapping rules
        mapping_rules = ioc.resolve(MappingRules)
        mapping_rules.add_rules()

        # dispatch route to function
        dispatcher = ioc.resolve(Dispatcher)
        route = event['routeKey']
        logger_factory().log_debug(f'Route: {route}')
        logger_factory().log_trace(f'Event: {event}')
        routes = dispatcher.dispatch_route_to_ctr
        response = PinfluencerResponse()
        if route not in routes:
            response = PinfluencerResponse(status_code=404, body={"message": f"route: {route} not found"})
        else:

            # initialize context which holds state for request/response through middlware
            pinfluencer_context = PinfluencerContext(response=response,
                                                     short_circuit=False,
                                                     event=event,
                                                     body={},
                                                     auth_user_id="",
                                                     route_key=route)
            route_desc: Route = routes[route]

            # middleware execution
            ioc.resolve(MiddlewarePipeline).execute_middleware(context=pinfluencer_context,
                                                               sequence=route_desc.sequence_builder)
    except Exception as e:
        logger_factory().log_error(str(e))
        response = PinfluencerResponse.as_500_error()
    logger_factory().log_debug(f"status: {response.status_code}")
    logger_factory().log_trace(f"output body: {response.body}")
    return response.as_json(serializer=ioc.resolve(Serializer))


def register_dependencies(cognito_auth_service, data_manager, ioc, middleware):
    ioc.add_instance(CognitoAuthService, cognito_auth_service)
    ioc.add_instance(DataManager, data_manager)
    ioc.add_singleton(Dispatcher)
    register_data_layer(ioc)
    register_domain(ioc)
    register_object_mapping(ioc)
    register_controllers(ioc)
    register_serialization(ioc)
    register_auth(ioc)
    register_middleware(ioc)
    register_sequences(ioc)
    ioc.add_instance(MiddlewarePipeline, middleware)
    ioc.add_singleton(FlexiUpdater)


    ioc.add_instance(Logger, logger_factory())
    ioc.add_instance(ServiceLocator, ServiceLocator(ioc=ioc))


def register_middleware(ioc):
    ioc.add_singleton(HooksFacade)
    ioc.add_singleton(CommonBeforeHooks)
    ioc.add_singleton(BrandAfterHooks)
    ioc.add_singleton(InfluencerAfterHooks)
    ioc.add_singleton(UserBeforeHooks)
    ioc.add_singleton(UserAfterHooks)
    ioc.add_singleton(InfluencerBeforeHooks)
    ioc.add_singleton(BrandBeforeHooks)
    ioc.add_singleton(ListingBeforeHooks)
    ioc.add_singleton(ListingAfterHooks)
    ioc.add_singleton(CommonAfterHooks)
    ioc.add_singleton(NotificationAfterHooks)
    ioc.add_singleton(NotificationBeforeHooks)
    ioc.add_singleton(AudienceCommonHooks)
    ioc.add_singleton(AudienceAgeBeforeHooks)
    ioc.add_singleton(AudienceAgeAfterHooks)
    ioc.add_singleton(AudienceGenderAfterHooks)
    ioc.add_singleton(AudienceGenderBeforeHooks)
    ioc.add_singleton(InfluencerOnBoardingAfterHooks)
    ioc.add_singleton(CollaborationBeforeHooks)
    ioc.add_singleton(CollaborationAfterHooks)


def register_auth(ioc):
    ioc.add_singleton(AuthUserRepository, CognitoAuthUserRepository)


def register_serialization(ioc):
    ioc.add_singleton(Deserializer, JsonCamelToSnakeCaseDeserializer)
    ioc.add_singleton(Serializer, JsonSnakeToCamelSerializer)


def register_controllers(ioc):
    ioc.add_singleton(BrandController)
    ioc.add_singleton(InfluencerController)
    ioc.add_singleton(ListingController)
    ioc.add_singleton(NotificationController)
    ioc.add_singleton(AudienceAgeController)
    ioc.add_singleton(AudienceGenderController)
    ioc.add_singleton(BrandListingController)
    ioc.add_singleton(InfluencerListingController)
    ioc.add_singleton(CollaborationController)


def register_object_mapping(ioc):
    ioc.add_singleton(PinfluencerObjectMapper)
    ioc.add_singleton(MappingRules)


def register_domain(ioc):
    ioc.add_singleton(BrandValidator)
    ioc.add_singleton(ListingValidator)
    ioc.add_singleton(InfluencerValidator)


def register_data_layer(ioc):
    # sql alchemy
    ioc.add_singleton(BrandRepository, SqlAlchemyBrandRepository)
    ioc.add_singleton(InfluencerRepository, SqlAlchemyInfluencerRepository)
    ioc.add_singleton(ListingRepository, SqlAlchemyListingRepository)
    ioc.add_singleton(NotificationRepository, SqlAlchemyNotificationRepository)
    ioc.add_singleton(AudienceAgeRepository, SqlAlchemyAudienceAgeRepository)
    ioc.add_singleton(AudienceGenderRepository, SqlAlchemyAudienceGenderRepository)
    ioc.add_singleton(BrandListingRepository, SqlAlchemyBrandListingRepository)
    ioc.add_singleton(InfluencerListingRepository, SqlAlchemyInfluencerListingRepository)
    ioc.add_singleton(CollaborationRepository, SqlAlchemyCollaborationRepository)

    # s3
    ioc.add_singleton(ImageRepository, S3ImageRepository)


def register_sequences(ioc: ServiceCollection):
    ioc.add_singleton(PreUpdateCreateListingSubsequenceBuilder)
    ioc.add_singleton(PreGenericUpdateCreateSubsequenceBuilder)
    ioc.add_singleton(PostSingleUserSubsequenceBuilder)
    ioc.add_singleton(PostMultipleUserSubsequenceBuilder)
    ioc.add_singleton(UpdateImageForListingSequenceBuilder)
    ioc.add_singleton(NotImplementedSequenceBuilder)
    ioc.add_singleton(UpdateListingSequenceBuilder)
    ioc.add_singleton(CreateListingSequenceBuilder)
    ioc.add_singleton(GetListingByIdSequenceBuilder)
    ioc.add_singleton(GetListingsForBrandSequenceBuilder)
    ioc.add_singleton(UpdateInfluencerImageSequenceBuilder)
    ioc.add_singleton(UpdateInfluencerSequenceBuilder)
    ioc.add_singleton(CreateInfluencerSequenceBuilder)
    ioc.add_singleton(GetAuthInfluencerSequenceBuilder)
    ioc.add_singleton(GetInfluencerByIdSequenceBuilder)
    ioc.add_singleton(GetAllInfluencersSequenceBuilder)
    ioc.add_singleton(UpdateBrandImageSequenceBuilder)
    ioc.add_singleton(UpdateBrandSequenceBuilder)
    ioc.add_singleton(CreateBrandSequenceBuilder)
    ioc.add_singleton(GetAuthBrandSequenceBuilder)
    ioc.add_singleton(GetBrandByIdSequenceBuilder)
    ioc.add_singleton(GetAllBrandsSequenceBuilder)
    ioc.add_singleton(CreateNotificationSequenceBuilder)
    ioc.add_singleton(GetNotificationByIdSequenceBuilder)
    ioc.add_singleton(CreateAudienceAgeSequenceBuilder)
    ioc.add_singleton(GetAudienceAgeSequenceBuilder)
    ioc.add_singleton(UpdateAudienceAgeSequenceBuilder)
    ioc.add_singleton(CreateAudienceGenderSequenceBuilder)
    ioc.add_singleton(GetAudienceGenderSequenceBuilder)
    ioc.add_singleton(UpdateAudienceGenderSequenceBuilder)
    ioc.add_singleton(CreateInfluencerProfileSequenceBuilder)
    ioc.add_singleton(UpdateInfluencerProfileSequenceBuilder)
    ioc.add_singleton(GetInfluencerProfileSequenceBuilder)
    ioc.add_singleton(GetBrandListingsForBrandSequenceBuilder)
    ioc.add_singleton(GetListingsForInfluencerSequenceBuilder)
    ioc.add_singleton(CreateCollaborationForInfluencerSequenceBuilder)