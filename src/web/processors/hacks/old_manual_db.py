import os

import boto3

rds_client = boto3.client('rds-data')

DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}


def execute_query(sql, sql_parameters=None):
    print(f'sql {sql}')
    print(f'sql parameters {sql_parameters}')
    if sql_parameters is None:
        sql_parameters = []
    response = rds_client.execute_statement(
        secretArn=DB_PARAMS['DB_SECRET_ARN'],
        database=DB_PARAMS['DATABASE_NAME'],
        resourceArn=DB_PARAMS['DB_CLUSTER_ARN'],
        sql=sql,
        parameters=sql_parameters
    )
    print(f'query response {response}')
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


# the order is important, index number is used in boto3 records lookup for json template creation
def build_json_for_brand(records) -> list[dict]:
    results = []
    for record in records:
        print(f'${record}')
        copy_brand = BRAND_TEMPLATE.copy()
        copy_brand['id'] = record[0]
        copy_brand['name'] = record[1]
        copy_brand['description'] = record[2]
        copy_brand['website'] = record[3]
        copy_brand['email'] = record[4]
        copy_brand['created'] = record[5]
        results.append(copy_brand)

    return results


# the order is important, index number is used in boto3 records lookup for json template creation
def build_json_for_product(records) -> list[dict]:
    results = []
    for record in records:
        copy_product = PRODUCT_TEMPLATE.copy()

        copy_brand = PRODUCT_TEMPLATE['brand'].copy()
        copy_product['id'] = record[0]
        copy_product['name'] = record[1]
        copy_product['description'] = record[2]
        copy_product['requirements'] = record[3]
        copy_brand['id'] = record[4]
        copy_brand['name'] = record[5]
        copy_product['brand'] = copy_brand
        copy_product['created'] = record[6]
        results.append(copy_product)

    return results


# the order is important, index number is used in boto3 records lookup for json template creation
COLUMNS_FOR_PRODUCT = ['id', 'name', 'description', 'requirements', 'brand_id', 'brand_name', 'created']

PRODUCT_TEMPLATE = {
    "id": "",
    "name": "",
    "description": "",
    "requirements": "",
    "brand": {
        "id": "",
        "name": ""
    },
    "created": ""
}

# the order is important, index number is used in boto3 records lookup for json template creation
COLUMNS_FOR_BRAND = ['id', 'name', 'description', 'website', 'email', 'auth_user_id', 'created']

BRAND_TEMPLATE = {
    "id": "",
    "name": "",
    "description": "",
    "created": ""
}
