import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # delete the todo from the database
    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    body = {
        'message': 'Deleted a TODO item with id {}'.format(event['pathParameters']['id'])
    }

    # create a response
    response = {
        'statusCode': 200,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    return response
