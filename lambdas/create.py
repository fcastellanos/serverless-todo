import boto3
import json
import os
import time
import uuid

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    data = json.loads(event['body'])

    if 'activity_title' not in data:
        print('Validation failed')

        body = { 'message': 'Validation failed' }

        return {
            "statusCode": 400,
            "body": json.dumps(body),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'activity_title': data['activity_title'],
        'activity_description': data['activity_description'],
        'date': data['date'],
        'time': data['time'],
        'period': data['period'],
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 201,
        "body": json.dumps(item),
        "headers": {
            "Content-Type": "application/json"
        }
    }

    return response
