import os

from simple_injection import ServiceCollection

from src import ServiceLocator
from src._types import DataManager, BrandRepository, InfluencerRepository, CampaignRepository, ImageRepository, \
    Deserializer, Serializer, AuthUserRepository, Logger, NotificationRepository
from src.crosscutting import JsonCamelToSnakeCaseDeserializer, JsonSnakeToCamelSerializer, \
    PinfluencerObjectMapper, FlexiUpdater, ConsoleLogger, DummyLogger
from src.data import SqlAlchemyDataManager
from src.data.repositories import SqlAlchemyBrandRepository, SqlAlchemyInfluencerRepository, \
    SqlAlchemyCampaignRepository, S3ImageRepository, CognitoAuthUserRepository, CognitoAuthService, \
    SqlAlchemyNotificationRepository
from src.domain.validation import BrandValidator, CampaignValidator, InfluencerValidator
from src.web import PinfluencerResponse, PinfluencerContext, Route
from src.web.controllers import BrandController, InfluencerController, CampaignController, NotificationController
from src.web.hooks import HooksFacade, CommonBeforeHooks, BrandAfterHooks, InfluencerAfterHooks, UserBeforeHooks, \
    UserAfterHooks, InfluencerBeforeHooks, BrandBeforeHooks, CampaignBeforeHooks, CampaignAfterHooks, CommonAfterHooks, \
    NotificationAfterHooks
from src.web.middleware import MiddlewarePipeline
from src.web.routing import Dispatcher
from src.web.sequences import PreGenericUpdateCreateSubsequenceBuilder, PreUpdateCreateCampaignSubsequenceBuilder, \
    PostSingleCampaignSubsequenceBuilder, PostMultipleCampaignSubsequenceBuilder, PostSingleUserSubsequenceBuilder, \
    PostMultipleUserSubsequenceBuilder, UpdateImageForCampaignSequenceBuilder, NotImplementedSequenceBuilder, \
    UpdateCampaignSequenceBuilder, CreateCampaignSequenceBuilder, GetCampaignByIdSequenceBuilder, \
    GetCampaignsForBrandSequenceBuilder, UpdateInfluencerImageSequenceBuilder, UpdateInfluencerSequenceBuilder, \
    CreateInfluencerSequenceBuilder, GetAuthInfluencerSequenceBuilder, GetInfluencerByIdSequenceBuilder, \
    GetAllInfluencersSequenceBuilder, UpdateBrandImageSequenceBuilder, UpdateBrandSequenceBuilder, \
    CreateBrandSequenceBuilder, GetAuthBrandSequenceBuilder, GetBrandByIdSequenceBuilder, GetAllBrandsSequenceBuilder, \
    CreateNotificationSequenceBuilder


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
    ioc.add_singleton(CampaignBeforeHooks)
    ioc.add_singleton(CampaignAfterHooks)
    ioc.add_singleton(CommonAfterHooks)
    ioc.add_singleton(NotificationAfterHooks)


def register_auth(ioc):
    ioc.add_singleton(AuthUserRepository, CognitoAuthUserRepository)


def register_serialization(ioc):
    ioc.add_singleton(Deserializer, JsonCamelToSnakeCaseDeserializer)
    ioc.add_singleton(Serializer, JsonSnakeToCamelSerializer)


def register_controllers(ioc):
    ioc.add_singleton(BrandController)
    ioc.add_singleton(InfluencerController)
    ioc.add_singleton(CampaignController)
    ioc.add_singleton(NotificationController)


def register_object_mapping(ioc):
    ioc.add_singleton(PinfluencerObjectMapper)


def register_domain(ioc):
    ioc.add_singleton(BrandValidator)
    ioc.add_singleton(CampaignValidator)
    ioc.add_singleton(InfluencerValidator)


def register_data_layer(ioc):
    # sql alchemy
    ioc.add_singleton(BrandRepository, SqlAlchemyBrandRepository)
    ioc.add_singleton(InfluencerRepository, SqlAlchemyInfluencerRepository)
    ioc.add_singleton(CampaignRepository, SqlAlchemyCampaignRepository)
    ioc.add_singleton(NotificationRepository, SqlAlchemyNotificationRepository)

    # s3
    ioc.add_singleton(ImageRepository, S3ImageRepository)


def register_sequences(ioc: ServiceCollection):
    ioc.add_singleton(PreGenericUpdateCreateSubsequenceBuilder)
    ioc.add_singleton(PreUpdateCreateCampaignSubsequenceBuilder)
    ioc.add_singleton(PostSingleCampaignSubsequenceBuilder)
    ioc.add_singleton(PostMultipleCampaignSubsequenceBuilder)
    ioc.add_singleton(PostSingleUserSubsequenceBuilder)
    ioc.add_singleton(PostMultipleUserSubsequenceBuilder)
    ioc.add_singleton(UpdateImageForCampaignSequenceBuilder)
    ioc.add_singleton(NotImplementedSequenceBuilder)
    ioc.add_singleton(UpdateCampaignSequenceBuilder)
    ioc.add_singleton(CreateCampaignSequenceBuilder)
    ioc.add_singleton(GetCampaignByIdSequenceBuilder)
    ioc.add_singleton(GetCampaignsForBrandSequenceBuilder)
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
