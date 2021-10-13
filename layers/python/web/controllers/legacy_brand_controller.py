import json
import uuid
import boto3
import os
import base64
try:
    from common import utils
    from data_access import db_common as db
except:
    from layers.python.common import utils
    from layers.python.data_access import db_common as db

DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}

REQUIRED_PAYLOAD_KEYS = ['name', 'bio', 'website', 'email']
COLUMNS = ['id', 'name', 'description', 'image_s3_key', 'brand_id']


def get_brands(event, context):
    try:
        print(event)
        try:
            selectQuery = "SELECT * FROM brand WHERE id=:id"
            id = event['queryStringParameters']['id']
            utils.validId(id)
            sql_parameters = [{'name': 'id', 'value': {'stringValue': id}}]
            result = executeQueryAndBuildResponse(selectQuery, sql_parameters)
            return result[0]
        except KeyError as missingKey:
            selectQuery = "SELECT * FROM brand"
            result = db.executeQuery(selectQuery, [], DB_PARAMS)
            body = buildJsonResponse(db.formatRecords(result['records']))
            for brand in body:
                selectQuery = "SELECT * FROM product WHERE brand_id=:brand_id"
                result = db.executeQuery(selectQuery, [{'name': 'brand_id', 'value': {'stringValue': brand["id"]}}],
                                         DB_PARAMS)
                productsTemplate = {"products": []}
                products = buildJsonResponse(db.formatRecords(result['records']))
                brand.update(productsTemplate)
                for product in products:
                    brand["products"].append(product)
            return {
                "headers": {
                    "Content-Type": "application/json"
                },
                'statusCode': 200,
                'body': json.dumps(body)
            }
        except utils.InvalidId as invalid:
            id = event['queryStringParameters']['id']
            if (id == "me"):
                auth_user_id = \
                (json.loads(base64.b64decode(event['headers']['authorization'].split(" ")[1].split(".")[1] + "===")))[
                    'cognito:username']
                selectQuery = "SELECT * FROM brand WHERE auth_user_id=:id"
                sql_parameters = [{'name': 'id', 'value': {'stringValue': auth_user_id}}]
                result = executeQueryAndBuildResponse(selectQuery, sql_parameters)
                if (result[1]):
                    return {
                        'statusCode': 404,
                        'body': 'no brand found for current user'
                    }
                else:
                    return result[0]
            else:
                print(invalid)
                return {
                    'statusCode': 400,
                    'body': ''
                }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }


def buildJsonResponse(body):
    result = list()

    print(body)
    for rowIndex, row in enumerate(body):
        result.append({})
        for index, columnValue in enumerate(row):
            result[rowIndex][COLUMNS[index]] = columnValue

    return result


def executeQueryAndBuildResponse(selectQuery, sql_parameters):
    result = db.executeQuery(selectQuery, sql_parameters, DB_PARAMS)
    body = buildJsonResponse(db.formatRecords(result['records']))
    return ({
                "headers": {
                    "Content-Type": "application/json"
                },
                'statusCode': 200,
                'body': json.dumps(body)
            }, len(body) == 0)


def post_brands(event, context):
    tokenPayload = event['requestContext']['authorizer']['jwt']['claims']

    if not 'body' in event:
        return {
            'statusCode': 400,
            'body': 'missing body'
        }

    body = json.loads(event['body'])

    if not valid(body, tokenPayload):
        return {
            'statusCode': 400,
            'body': f'Required keys in body {REQUIRED_PAYLOAD_KEYS}, body received {body}'
        }

    sql = "SELECT * FROM brand WHERE auth_user_id=:auth_user_id"
    sql_parameters = [{'name': 'auth_user_id', 'value': {'stringValue': tokenPayload['cognito:username']}}]
    response = db.executeQuery(sql, sql_parameters, DB_PARAMS)
    if (len(response['records']) >= 1):
        return {
            'statusCode': 400,
            'body': "two brands cannot be associated with same auth user"
        }

    sql = "INSERT INTO brand(id, name, bio, website, email, auth_user_id) VALUES (:id, :name, :bio, :website, :email, :auth_user_id)"
    id = str(uuid.uuid4())
    sql_parameters = [
        {'name': 'id', 'value': {'stringValue': id}},
        {'name': 'name', 'value': {'stringValue': body['name']}},
        {'name': 'bio', 'value': {'stringValue': body['bio']}},
        {'name': 'website', 'value': {'stringValue': body['website']}},
        {'name': 'email', 'value': {'stringValue': getEmail(body, tokenPayload)}},
        {'name': 'auth_user_id', 'value': {'stringValue': tokenPayload['cognito:username']}}
    ]

    try:
        response = db.executeQuery(sql, sql_parameters, DB_PARAMS)
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

    print(f'Number of records updated: {response["numberOfRecordsUpdated"]}')

    return {
        'statusCode': 201,
        'body': id
    }


def valid(body, tokenPayload):
    return (list(body.keys()) == ['name', 'bio', 'website', 'email']) or (
                'email' in tokenPayload and list(body.keys()) == ['name', 'bio', 'website'])


def getEmail(body, tokenPayload):
    if ('email' in body):
        return body['email']
    else:
        return tokenPayload['email']