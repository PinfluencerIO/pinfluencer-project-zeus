from src.crosscutting import print_exception
from src.web import PinfluencerResponse
from src.web.routes import Routes


def lambda_handler(event, context):
    routes = Routes()
    try:
        print(f'route: {event["routeKey"]}')
        print(f'event: {event}')
        response = routes.routes[event['routeKey']](event)
        return response.as_json()
    except KeyError as ke:
        print(f'Missing required key {ke}')
        return PinfluencerResponse.as_400_error().as_json()
    except Exception as e:
        print_exception(e)
        return PinfluencerResponse.as_500_error().as_json()
