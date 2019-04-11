import logging
import os
import time

import redis
import requests
from applicationinsights.flask.ext import AppInsights
from flask import Flask, Response, request

INSTRUMENTATION_KEY = '115fcb01-ff5c-42db-9b69-5e6ae017f9a7'

app = Flask(__name__)
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = INSTRUMENTATION_KEY

# log requests, traces and exceptions to the Application Insights service
appinsights = AppInsights(app)

role_name = os.getenv('APPINSIGHTS_ROLE_NAME', 'rbc-devops-sample-dev')
role_instance = os.getenv('APPINSIGHTS_ROLE_INSTANCE', 'foobar')
appinsights.context.cloud.role = role_name
appinsights.context.cloud.role_instance = role_instance


@app.route('/')
def hello_world():
    app.logger.warning(f'Logging request headers:\n{str(request.headers)}.')

    logging.error('Testing error logging...')
    return 'Hello, World!'


@app.route('/snail')
def slow():
    app.logger.warning('This API is sooooo slow!!!')
    time.sleep(40)
    app.logger.info('making an API request to ')
    return "I'm ALIVE!"


@app.route('/dad-joke')
def dad_joke():
    app.logger.warning(f'Logging request headers:\n{str(request.headers)}.')

    request_id = request.headers.get('Request-Id', 'NO-REQUEST-ID')
    app.logger.warning(f'Current request ID is {request_id}.')

    app.logger.debug('making a request to the Dad Jokes API')
    response = requests.get('https://icanhazdadjoke.com', headers={"Accept": "text/plain"})
    return response.content


@app.route('/dad-joke-internal')
def dad_joke_internal():
    app.logger.warning(f'Logging request headers:\n{str(request.headers)}.')

    request_id = request.headers.get('Request-Id', 'NO-REQUEST-ID')
    app.logger.warning(f'Current request ID is {request_id}.')

    other_service_url = "https://rbc-devops-sample-dev.azurewebsites.net/dad-joke"
    app.logger.info('Calling the other service')
    response = requests.get(
        other_service_url,
        headers={
            'Correlation-Context': f'operation_Id={request_id}',
            'Request-Context': f'operation_Id={request_id}',
        }
    )
    return response.content


@app.route('/403')
def four_oh_three():
    app.logger.warning('This guy is not authorized to access. WATCH HIM!')
    return Response(status=403)


@app.route('/500')
def five_hundred():
    app.logger.error('Oops! Something went wrong :)')
    return Response(status=500)


@app.route('/throw')
def throw_unhandled():
    app.logger.error("OH NO! Can't handle this...")
    raise Exception('blah')


@app.route('/redis')
def do_redis():
    app.logger.error("Connecting to Redis instance...")
    r = redis.Redis(host='rbc-devops-test-app.redis.cache.windows.net',
                    password='LrhN7kuMUokdOaP8njaw9ctpRpWdLFhayDOUv25iSgs=',
                    port=6379, db=0)
    r.set('foobar', 'baz')
    value = r.get('foobar')
    return value


PORT = os.getenv('PORT', 80)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
