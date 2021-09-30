import json
import utils
import db_common

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "product post"
        }),
    }
