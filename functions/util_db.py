import boto3
import os

DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}

rds_client = boto3.client('rds-data')


class Repository:
    @staticmethod
    def create(resource, data):
        pass

    @staticmethod
    def get_by_id(resource, id):
        pass

    @staticmethod
    def get_all(resource):
        return format_records(execute_query(f'SELECT * FROM {resource}')['records'])

    @staticmethod
    def update(resource, data):
        pass

    @staticmethod
    def delete(resource):
        pass


def execute_query(sql, sql_parameters=None):
    if sql_parameters is None:
        sql_parameters = []
    response = rds_client.execute_statement(
        secretArn=DB_PARAMS['DB_SECRET_ARN'],
        database=DB_PARAMS['DATABASE_NAME'],
        resourceArn=DB_PARAMS['DB_CLUSTER_ARN'],
        sql=sql,
        parameters=sql_parameters
    )

    return response


def format_field(field):
    if list(field.keys())[0] != 'isNull':
        return list(field.values())[0]
    else:
        return ""


def format_record(record):
    return [format_field(field) for field in record]


def format_records(records):
    return [format_record(record) for record in records]
