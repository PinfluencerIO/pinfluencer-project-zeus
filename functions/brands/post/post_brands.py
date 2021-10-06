import json
import uuid
import boto3
import os
try:
    import db_common as db
except:
    from layers.python import db_common as db


DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}

rds_client = boto3.client('rds-data')
REQUIRED_PAYLOAD_KEYS = ['name', 'bio', 'website', 'email']

def lambda_handler(event, context):
    
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
    sql_parameters = [{'name':'auth_user_id', 'value':{'stringValue': tokenPayload['cognito:username']}}]
    response = db.executeQuery(sql, sql_parameters,DB_PARAMS)
    if(len(response['records']) >= 1):
        return {
            'statusCode': 400,
            'body': "two brands cannot be associated with same auth user"
        }
    
    sql = "INSERT INTO brand(id, name, bio, website, email, auth_user_id) VALUES (:id, :name, :bio, :website, :email, :auth_user_id)"
    id = str(uuid.uuid4())
    sql_parameters = [
        {'name':'id', 'value':{'stringValue': id}},
        {'name':'name', 'value':{'stringValue': body['name']}},
        {'name':'bio', 'value':{'stringValue': body['bio']}},
        {'name':'website', 'value':{'stringValue': body['website']}},
        {'name':'email', 'value':{'stringValue': getEmail(body, tokenPayload)}},
        {'name':'auth_user_id', 'value':{'stringValue': tokenPayload['cognito:username']}}
    ]
    
    try:
        response = db.executeQuery(sql, sql_parameters,DB_PARAMS)
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
    return (list(body.keys()) == ['name', 'bio', 'website', 'email']) or ('email' in tokenPayload and list(body.keys()) == ['name', 'bio', 'website'])

def getEmail(body, tokenPayload):
    if('email' in body):
        return body['email']
    else:
        return tokenPayload['email']