from src.container import Container
from src.log_util import print_exception
from src.pinfluencer_response import PinfluencerResponse
from src.routes import Routes


def lambda_handler(event, context):
    container = Container()
    routes = Routes(container.data_manager, container.image_repository)
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
