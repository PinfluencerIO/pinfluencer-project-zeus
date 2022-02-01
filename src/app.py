from src.crosscutting import print_exception
from src.web import PinfluencerResponse
from src.web.routing import Dispatcher


def lambda_handler(event, context):
    dispatcher = Dispatcher()
    try:
        route = event['routeKey']
        print(f'Route: {route}')
        print(f'Event: {event}')
        response = dispatcher.dispatch_route_to_ctr[route](event)
        return response.as_json()
    except KeyError as ke:
        print(f'Missing required key {ke}')
        return PinfluencerResponse.as_400_error().as_json()
    except Exception as e:
        print_exception(e)
        return PinfluencerResponse.as_500_error().as_json()
