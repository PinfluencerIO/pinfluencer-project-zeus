import datetime
import uuid

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
        data['id'] = str(uuid.uuid4())
        dt = datetime.datetime.utcnow()
        print(dt)
        data['created'] = str(dt)
        data['version'] = 1

        sql, sql_parameters = Repository._create_brand_query_builders(data, resource)

        Repository._execute_query(sql, sql_parameters)

        return data['id']

    @staticmethod
    def get_by_id(resource, id_):
        pass

    @staticmethod
    def get_all(resource):
        return Repository._format_records(Repository._execute_query(f'SELECT * FROM {resource}')['records'])

    @staticmethod
    def update(resource, data):
        pass

    @staticmethod
    def delete(resource):
        pass

    @staticmethod
    def _create_brand_query_builders(data, resource):
        sql = f'INSERT INTO {resource}(id, created, name, description, website, email, version, auth_user_id) ' \
              f'VALUES(:id, :created, :name, :description, :website, :email, :version, :auth_user_id)'
        sql_parameters = [
            {'name': 'id', 'value': {'stringValue': data['id']}},
            {'name': 'created', 'value': {'stringValue': data['created']}},
            {'name': 'version', 'value': {'longValue': data['version']}},
            {'name': 'name', 'value': {'stringValue': data['name']}},
            {'name': 'description', 'value': {'stringValue': data['description']}},
            {'name': 'website', 'value': {'stringValue': data['website']}},
            {'name': 'email', 'value': {'stringValue': data['email']}},
            {'name': 'auth_user_id', 'value': {'stringValue': data['auth_user']}}
        ]
        return sql, sql_parameters

    @staticmethod
    def _execute_query(sql, sql_parameters=None):
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

    @staticmethod
    def _format_field(field):
        if list(field.keys())[0] != 'isNull':
            return list(field.values())[0]
        else:
            return ""

    @staticmethod
    def _format_record(record):
        return [Repository._format_field(field) for field in record]

    @staticmethod
    def _format_records(records):
        return [Repository._format_record(record) for record in records]

