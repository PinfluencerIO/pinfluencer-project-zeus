import boto3
import os

DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}

rds_client = boto3.client('rds-data')

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

def executeQuery(sql, sql_parameters=[]):
    response = rds_client.execute_statement(
        secretArn= DB_PARAMS['DB_SECRET_ARN'],
        database=DB_PARAMS['DATABASE_NAME'],
        resourceArn=DB_PARAMS['DB_CLUSTER_ARN'],
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