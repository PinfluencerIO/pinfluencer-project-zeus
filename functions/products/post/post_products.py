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
    from layers.python import utilss

DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}

s3 = boto3.client('s3')

REQUIRED_PAYLOAD_KEYS = ['name', 'description', 'image_filename', 'image_bytes']

def lambda_handler(event, context):
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
        records = db.executeQuery("SELECT * FROM brand WHERE auth_user_id=:id", [{'name':'id', 'value':{'stringValue': auth_user_id}}], DB_PARAMS)
        brand_id = db.formatRecords(records['records'])[0][0]
        product_id = str(uuid.uuid4())
        filename = body['image_filename']
        image = base64.b64decode(body['image_bytes'])
    
        key= f'{brand_id}/{product_id}/{filename}'
        
        s3.put_object(Bucket='pinfluencer-product-images', Key=key, Body=image, ContentType=f'image/{filename[-3:]}', Tagging='public=yes')
        
        sql = "INSERT INTO product(id, name, description, image_s3_key, brand_id) VALUES (:id, :name, :description, :image_s3_key, :brand_id)"
        sql_parameters = [
            {'name':'id', 'value':{'stringValue': product_id}},
            {'name':'name', 'value':{'stringValue': body['name']}},
            {'name':'description', 'value':{'stringValue': body['description']}},
            {'name':'image_s3_key', 'value':{'stringValue': filename}},
            {'name':'brand_id', 'value':{'stringValue': brand_id}}
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
