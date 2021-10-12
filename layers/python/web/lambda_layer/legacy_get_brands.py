import json
import os
from layers.python.common import utils
from layers.python.data_access import db_common as db
import base64

DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}

COLUMNS = ['id', 'name', 'bio', 'website', 'email', 'auth_user_id']


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
            'body': str(DB_PARAMS)
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