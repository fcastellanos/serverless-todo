import json
import os
import jwt
import time
from auth_header import AuthHeader

def handler(event, context):
    request_body = json.loads(event['body'])
    jwt_secret   = os.environ['todo_jwt_secret']
    auth_header  = AuthHeader(event['headers']['Authorization'])

    print("Auth token => {}".format(auth_header.token))

    # TODO: Verify token

    payload = {
        'exp': get_expiration_hrs(1),
        'iss': 'python-tijuana',
    }

    token = jwt.encode(payload, jwt_secret, algorithm='HS256')

    body = {
        'token': token,
        'expires_at': payload['exp']
    }

    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }

def get_expiration_hrs(hrs):
    seconds = hrs * 3600
    stamp   = time.time() + seconds

    return int(stamp)
