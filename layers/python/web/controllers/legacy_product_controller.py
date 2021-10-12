import base64
import json
import os
import uuid

try:
    import data_access.db_common as db
except:
    pass

try:
    import common.utils
except:
    from layers.python.common import utils
    from layers.python.data_access import db_common as db

DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}

COLUMNS = ['id', 'name', 'description', 'image_s3_key', 'brand_id']
REQUIRED_PAYLOAD_KEYS = ['name', 'description', 'image_filename', 'image_bytes']

s3 = boto3.client('s3')


def get_products(event, context):
    tokenPayload = event['requestContext']['authorizer']['jwt']['claims']
    try:
        sql, parameters = buildSelectStatement(event, tokenPayload)
        result = db.executeQuery(sql, parameters, DB_PARAMS)

        body = db.formatRecords(result['records'])

        result = buildJsonResponse(body)

        return {
            "headers": {
                "Content-Type": "application/json"
            },
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except utils.InvalidId as invalidId:
        print(invalidId)
        return {
            'statusCode': 400,
            'body': 'bad id'
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }


def buildJsonResponse(body):
    result = list()

    for rowIndex, row in enumerate(body):
        result.append({})
        for index, columnValue in enumerate(row):
            result[rowIndex][COLUMNS[index]] = columnValue

    return result


# Builds a statement based on query string.
# id for individual product
# token 'cognito:username' for all products related to brand
def buildSelectStatement(event, tokenPayload):
    if validProductId(event):
        utils.validId(event['queryStringParameters']['id'])
        id = event['queryStringParameters']['id']
        return "SELECT * FROM product WHERE id=:id", [{'name': 'id', 'value': {'stringValue': id}}]
    else:
        auth_user_id = tokenPayload['cognito:username']

        records = db.executeQuery("SELECT * FROM brand WHERE auth_user_id=:id",
                                  [{'name': 'id', 'value': {'stringValue': auth_user_id}}], DB_PARAMS)

        id = db.formatRecords(records['records'])[0][0]

        return "SELECT * FROM product WHERE brand_id=:id", [{'name': 'id', 'value': {'stringValue': id}}]


# Validates if event query string parameter has an id key
def validProductId(event):
    return 'queryStringParameters' in event and 'id' in event['queryStringParameters']


def post_products(event, context):
    try:
        if not 'body' in event:
            return {
                'statusCode': 400,
                'body': 'missing body'
            }

        body = json.loads(event['body'])
        if not valid(body):
            return {
                'statusCode': 400,
                'body': f'The body is either missing required keys, or a value is incorrect'
            }
        tokenPayload = event['requestContext']['authorizer']['jwt']['claims']
        auth_user_id = tokenPayload['cognito:username']
        records = db.executeQuery("SELECT * FROM brand WHERE auth_user_id=:id",
                                  [{'name': 'id', 'value': {'stringValue': auth_user_id}}], DB_PARAMS)
        brand_id = db.formatRecords(records['records'])[0][0]
        product_id = str(uuid.uuid4())
        filename = body['image_filename']
        image = base64.b64decode(body['image_bytes'])

        key = f'{brand_id}/{product_id}/{filename}'

        s3.put_object(Bucket='pinfluencer-product-images', Key=key, Body=image, ContentType=f'image/{filename[-3:]}',
                      Tagging='public=yes')

        sql = "INSERT INTO product(id, name, description, image_s3_key, brand_id) VALUES (:id, :name, :description, :image_s3_key, :brand_id)"
        sql_parameters = [
            {'name': 'id', 'value': {'stringValue': product_id}},
            {'name': 'name', 'value': {'stringValue': body['name']}},
            {'name': 'description', 'value': {'stringValue': body['description']}},
            {'name': 'image_s3_key', 'value': {'stringValue': filename}},
            {'name': 'brand_id', 'value': {'stringValue': brand_id}}
        ]

        try:
            response = db.executeQuery(sql, sql_parameters, DB_PARAMS)

            print(f'Number of records updated: {response["numberOfRecordsUpdated"]}')

            return {
                'statusCode': 201,
                'body': product_id
            }
        except Exception as e:
            print(e)
            return {
                'statusCode': 500,
                'body': 'Server error'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }


def valid(body):
    return list(body.keys()) == REQUIRED_PAYLOAD_KEYS
