import boto3
import mock
import os
import json

from sure import expect
from moto import mock_dynamodb
from contextlib import contextmanager

from lambdas import create

@contextmanager
def test_setup():
    with mock_dynamodb():
        setup_dynamodb()
        yield

def setup_dynamodb():
    dynamodb = boto3.resource('dynamodb')

    dynamodb.create_table(
        TableName='test_table',
        AttributeDefinitions=[
            {'AttributeName': 'id',
            'AttributeType': 'S'}
        ],
        KeySchema=[
            {'AttributeName': 'id',
            'KeyType': 'HASH'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

def test_create():
    with test_setup():
        event = {
            'body': json.dumps({
                	'activity_title': 'Test me',
                	'activity_description': 'please',
                	'date': '01-10-2019',
                	'time': '8:00',
                	'period': 'am'
            })
        }

        k = mock.patch.dict(os.environ, {'DYNAMODB_TABLE': 'test_table'})
        k.start()

        response = optin.handler(event, {})

        expected_status = 201

        k.stop()

        expect(response['statusCode']).to.equal(expected_status)
