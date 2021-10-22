import os

import boto3


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


def build_json_from_db_records(body, cols):
    result = list()

    for rowIndex, row in enumerate(body):
        result.append({})
        for index, columnValue in enumerate(row):
            if cols[index] == 'image':
                result[rowIndex]['image'] = {"filename": columnValue}
            else:
                result[rowIndex][cols[index]] = columnValue

    print(result)

    return result


DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}
rds_client = boto3.client('rds-data')


def find_brand_by_auth_user(event):
    user = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
    sql = "SELECT id, name FROM brand WHERE auth_user_id=:auth_user_id"
    sql_parameters = [{'name': 'auth_user_id', 'value': {'stringValue': user}}]
    result = execute_query(sql, sql_parameters)
    return result, user
