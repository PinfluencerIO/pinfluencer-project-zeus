import json
import uuid
import boto3
import os
import base64
try:
    import db_common as db
except:
    from layers.python import db_common as db

try:
    import utils
except:
    from layers.python import utils

DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}

COLUMNS = ['id', 'name', 'description', 'image_s3_key', 'brand_id']

def lambda_handler(event, context):
    tokenPayload = event['requestContext']['authorizer']['jwt']['claims']
    try:
        sql, parameters = buildSelectStatement(event,tokenPayload)
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
def buildSelectStatement(event,tokenPayload):
    if validProductId(event):
        utils.validId(event['queryStringParameters']['id'])
        id = event['queryStringParameters']['id']
        return "SELECT * FROM product WHERE id=:id", [{'name':'id', 'value':{'stringValue': id}}]
    else:
        auth_user_id = tokenPayload['cognito:username']
        
        records = db.executeQuery("SELECT * FROM brand WHERE auth_user_id=:id", [{'name':'id', 'value':{'stringValue': auth_user_id}}], DB_PARAMS)
        
        id = db.formatRecords(records['records'])[0][0]
        
        return "SELECT * FROM product WHERE brand_id=:id", [{'name':'id', 'value':{'stringValue': id}}]

# Validates if event query string parameter has an id key
def validProductId(event):
    return 'queryStringParameters' in event and 'id' in event['queryStringParameters']
