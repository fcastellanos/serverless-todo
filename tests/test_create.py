import boto3
import mock
import os
import json
import pytest

from lambdas import create

from sure import expect
from moto import mock_dynamodb2
from contextlib import contextmanager

@contextmanager
def db_setup():
    with mock_dynamodb2():
        setup_dynamodb()
        yield

def setup_dynamodb():
    dynamodb = boto3.resource('dynamodb')

    dynamodb.create_table(
        TableName='test_table',
        AttributeDefinitions=[
            { 'AttributeName': 'id', 'AttributeType': 'S' }
        ],
        KeySchema=[
            { 'AttributeName': 'id', 'KeyType': 'HASH' }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

def test_create():
    with db_setup():
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

        response = create.handler(event, {})
        response_body = json.loads(response['body'])

        expected_status = 201

        k.stop()
        # pytest.set_trace()
        expect(response['statusCode']).to.equal(expected_status)
        expect(response_body['activity_title']).to.equal('Test me')
