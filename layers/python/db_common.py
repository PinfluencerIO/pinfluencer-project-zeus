import os
import boto3

rds_client = boto3.client('rds-data')

# Executes a sql statement against configured db
def executeQuery(sql, sql_parameters=[], db_parameters={}):
    response = rds_client.execute_statement(
        secretArn= db_parameters['DB_SECRET_ARN'],
        database=db_parameters['DATABASE_NAME'],
        resourceArn=db_parameters['DB_CLUSTER_ARN'],
        sql=sql,
        parameters=sql_parameters
    )
    return response

# Formatting query returned Field
def formatField(field):
  if list(field.keys())[0] != 'isNull':
    return list(field.values())[0]
  else:
    return ""
   
# Formatting query returned Record
def formatRecord(record):
   return [formatField(field) for field in record]
   
# Formatting query returned Field
def formatRecords(records):
   return [formatRecord(record) for record in records]