from mapper.object_mapper import ObjectMapper
from simple_injection import ServiceCollection

from src._types import DataManager, BrandRepository, InfluencerRepository, CampaignRepository, ImageRepository, \
    ObjectMapperAdapter, Deserializer, Serializer, AuthUserRepository
from src.crosscutting import print_exception, JsonCamelToSnakeCaseDeserializer, JsonSnakeToCamelSerializer
from src.data import SqlAlchemyDataManager
from src.data.repositories import SqlAlchemyBrandRepository, SqlAlchemyInfluencerRepository, \
    SqlAlchemyCampaignRepository, S3ImageRepository, CognitoAuthUserRepository, CognitoAuthService
from src.domain.validation import BrandValidator, CampaignValidator, InfluencerValidator
from src.web import PinfluencerResponse, PinfluencerContext, Route, PinfluencerAction
from src.web.controllers import BrandController, InfluencerController, CampaignController
from src.web.hooks import HooksFacade, CommonBeforeHooks, BrandAfterHooks, InfluencerAfterHooks, UserBeforeHooks, \
    UserAfterHooks, InfluencerBeforeHooks, BrandBeforeHooks, CampaignBeforeHooks, CampaignAfterHooks, CommonAfterHooks
from src.web.middleware import MiddlewarePipeline
from src.web.routing import Dispatcher


def lambda_handler(event, context):
    return bootstrap(event=event,
                     context=context,

                     # infra for testability
                     middleware=MiddlewarePipeline(),
                     ioc=ServiceCollection(),
                     data_manager=SqlAlchemyDataManager(),
                     cognito_auth_service=CognitoAuthService())


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
        print(f'Route: {route}')
        print(f'Event: {event}')
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
                                                     auth_user_id="")
            route_desc: Route = routes[route]

            # middleware execution
            middleware_pipeline: list[PinfluencerAction] = [*route_desc.before_hooks, route_desc.action, *route_desc.after_hooks]
            ioc.resolve(MiddlewarePipeline).execute_middleware(context=pinfluencer_context,
                                                                            middleware=middleware_pipeline)
    except Exception as e:
        print_exception(e)
        response = PinfluencerResponse.as_500_error()
    print(f"status: {response.status_code}")
    print(f"output body: {response.body}")
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
    ioc.add_instance(MiddlewarePipeline, middleware)


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


def register_auth(ioc):
    ioc.add_singleton(AuthUserRepository, CognitoAuthUserRepository)


def register_serialization(ioc):
    ioc.add_singleton(Deserializer, JsonCamelToSnakeCaseDeserializer)
    ioc.add_singleton(Serializer, JsonSnakeToCamelSerializer)


def register_controllers(ioc):
    ioc.add_singleton(BrandController)
    ioc.add_singleton(InfluencerController)
    ioc.add_singleton(CampaignController)


def register_object_mapping(ioc):
    mapper = ObjectMapper()
    ioc.add_instance(ObjectMapperAdapter, mapper)


def register_domain(ioc):
    ioc.add_singleton(BrandValidator)
    ioc.add_singleton(CampaignValidator)
    ioc.add_singleton(InfluencerValidator)


def register_data_layer(ioc):

    # sql alchemy
    ioc.add_singleton(BrandRepository, SqlAlchemyBrandRepository)
    ioc.add_singleton(InfluencerRepository, SqlAlchemyInfluencerRepository)
    ioc.add_singleton(CampaignRepository, SqlAlchemyCampaignRepository)

    # s3
    ioc.add_singleton(ImageRepository, S3ImageRepository)
