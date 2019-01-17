## Simple Serverless TODO

Simple Serverless TODO API example built with Python 3.6 made to run in AWS Lambda.

The goal of this repository is to showcase a serverless framework stack written in Python (3.6) with tests (pytest, sure, moto), simple JWT authentication with lambda authorizer and DynamoDB as the database.

Interesting features:
- serverless-python-requirements plugin
  * dockerizePip
  * slim
  * noDeploy
- Excluding packages
- Parameter store (ssm)
- Travis-CI
- Connect to a different AWS API Gateway
- Lambda authorizer (JWT)

[![Build Status](https://travis-ci.org/fcastellanos/serverless-todo.svg?branch=master)](https://travis-ci.org/fcastellanos/serverless-todo)
