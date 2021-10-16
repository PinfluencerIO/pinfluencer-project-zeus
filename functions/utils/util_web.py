import utils.util_log as log
import utils.util_http as http
import utils.util_db as db

class Controller():
    def __init__(self):
        pass

    @staticmethod
    def process(event):
        try:
            http_method = Controller.extract_http_method(event)
            resource = event['rawPath'][1:-1]
            # Handle CRUD 
            if http_method == 'post':
                return http.HttpUtils.respond(res=f"Create {resource}")
            elif http_method == 'get':
                formatted = db.formatRecords(db.executeQuery(f'SELECT * FROM {resource}')['records'])
                return http.HttpUtils.respond(res=f"Read {resource} Results:\n {formatted}")
            elif http_method == 'put':
                return http.HttpUtils.respond(res=f"Update {resource}")
            elif http_method == 'delete':
                return http.HttpUtils.respond(res=f"Delete {resource}")

            return http.HttpUtils.respond(err="Unsupported action", err_code=400, res=f"Unsupported action {http_method}")

        except Exception as e:
            log.print_exception(e)
            return http.HttpUtils.respond(err=e, err_code=404)

    @staticmethod
    def extract_http_method(event):
        return event['requestContext']['http']['method'].lower()
