from src.crosscutting import print_exception
from src.web import PinfluencerResponse, PinfluencerContext, Route, PinfluencerAction
from src.web.ioc import ServiceLocator
from src.web.routing import Dispatcher


def lambda_handler(event, context):
    return bootstrap(event=event,
                     context=context,
                     service_locator=ServiceLocator())


def bootstrap(event: dict,
              context: dict,
              service_locator: ServiceLocator) -> dict:
    dispatcher = Dispatcher(service_locator=service_locator)
    try:
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
            service_locator.get_new_middlware_pipeline().execute_middleware(context=pinfluencer_context,
                                                                            middleware=middleware_pipeline)
    except Exception as e:
        print_exception(e)
        response = PinfluencerResponse.as_500_error()
    print(f"output body: {response.body}")
    return response.as_json(serializer=service_locator.get_new_serializer())
