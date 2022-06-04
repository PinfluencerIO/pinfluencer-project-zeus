from src.crosscutting import print_exception
from src.service import ServiceLocator
from src.web import PinfluencerResponse
from src.web.routing import Dispatcher


def lambda_handler(event, context):
    bootstrap(event=event,
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
        if route not in routes:
            response = PinfluencerResponse(status_code=404, body={"message": f"route: {route} not found"})
        else:
            response = routes[route](event)
    except Exception as e:
        print_exception(e)
        response = PinfluencerResponse.as_500_error()
    print(f"output body: {response.body}")
    return response.as_json(serializer=service_locator.get_new_serializer())
