import boto3
import json
import os
import lambdas.decimalencoder as decimalencoder

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Fetch all todos from the database
    result = table.scan()

    # Create a response
    response = {
        'statusCode': 200,
        'body': json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    return response
