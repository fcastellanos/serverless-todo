import os
import re
import json
from datetime import datetime
import jwt

from lambdas.auth_header import AuthHeader
from lambdas.http_verb import HttpVerb
from lambdas.auth_policy import AuthPolicy

# NOTE: For more info on lambda authorizers go to
# https://github.com/awslabs/aws-apigateway-lambda-authorizer-blueprints

def handler(event, context):
    jwt_secret  = os.environ['todo_jwt_secret']
    auth_header = AuthHeader(event['authorizationToken'])

    # NOTE: Basically if we can decode the token it means that the client produced
    # a token with the JWT secret and it should be allowed to use the API
    try:
        payload = jwt.decode(auth_header.token, jwt_secret, algorithms=['HS256'])
    except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidIssuerError) as err:
        # NOTE: If the token could not be decoded it raises an Exception, we catch it
        # log the error and raise an Unauthorized exception
        raise Exception('Unauthorized')

    # NOTE: After the token is decoded we proceed to generate an AuthPolicy document
    # to return as the authorizer response
    principalId = 'jwt|{0}'.format(auth_header.token)

    tmp = event['methodArn'].split(':')
    apiGatewayArnTmp = tmp[5].split('/')
    awsAccountId = tmp[4]

    policy = AuthPolicy(principalId, awsAccountId)
    policy.restApiId = apiGatewayArnTmp[0]
    policy.region = tmp[3]
    policy.stage = apiGatewayArnTmp[1]

    policy.allowMethod(HttpVerb.GET, '/*')
    policy.allowMethod(HttpVerb.POST, '/*')
    policy.allowMethod(HttpVerb.PUT, '/*')
    policy.allowMethod(HttpVerb.DELETE, '/*')

    # Finally, build the policy
    authResponse = policy.build()

    return authResponse
