import json
import logging
import boto3

rds_client = boto3.client('rds-data')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print(event)
    response = Controller.process(event)
    logger.info("response: %s" % response)
    return response


class Controller():
    def __init__(self):
        pass

    @staticmethod
    def process(event):
        try:
            http_method = event['requestContext']['http']['method'].lower()
            resource = event['rawPath'][1:]
            # Handle CRUD 
            if http_method == 'post':
                return HttpUtils.respond(res=f"Create {resource}")
            elif http_method == 'get':
                return HttpUtils.respond(res=f"Read {resource}")
            elif http_method == 'put':
                return HttpUtils.respond(res=f"Update {resource}")
            elif http_method == 'delete':
                return HttpUtils.respond(res=f"Delete {resource}")

            return HttpUtils.respond(err="Unsupported action", err_code=400, res=f"Unsupported action {http_method}")

        except Exception as e:
            print_exception(e)
            return HttpUtils.respond(err=e, err_code=404)

class HttpUtils:
    def __init__(self):
        pass

    @staticmethod
    def respond(err=None, err_code=400, res=None):
        return {
            'statusCode': str(err_code) if err else '200',
            'body': '{"message":%s}' % json.dumps(str(err)) if err else res,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }

class Respository:
    def __init__(self) -> None:
        pass

    def create(resource, data):
        pass

    def get_by_id(resource, id):
        pass

    def get_all(resource):
        pass
    
    def update(resource, data):
        pass

    def delete(resource):
        pass


def executeQuery(sql, sql_parameters=[], db_parameters={}):
    response = rds_client.execute_statement(
        secretArn= db_parameters['DB_SECRET_ARN'],
        database=db_parameters['DATABASE_NAME'],
        resourceArn=db_parameters['DB_CLUSTER_ARN'],
        sql=sql,
        parameters=sql_parameters
    )
    return response

def formatField(field):
  if list(field.keys())[0] != 'isNull':
    return list(field.values())[0]
  else:
    return ""
   
def formatRecord(record):
   return [formatField(field) for field in record]
   
def formatRecords(records):
   return [formatRecord(record) for record in records]

def print_exception(e):
    logger.error(''.join(['Exception ', str(type(e))]))
    logger.error(''.join(['Exception ', str(e)]))