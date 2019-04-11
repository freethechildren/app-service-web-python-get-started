import logging
import os
import time
import redis
import requests
import json
from applicationinsights.flask.ext import AppInsights
from flask import Flask, Response, request


PORT = os.getenv('PORT', 80)
role_key = os.getenv('APPINSIGHTS_INSTRUMENTATIONKEY', '')
role_name = os.getenv('APPINSIGHTS_ROLE_NAME', '')
role_instance = os.getenv('APPINSIGHTS_ROLE_INSTANCE', '')


# log requests, traces and exceptions to the Application Insights service
app = Flask(__name__)
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = role_key
appinsights = AppInsights(app)
appinsights.context.cloud.role = role_name
appinsights.context.cloud.role_instance = role_instance


@app.route('/')
def hello_world():
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
    app.logger.debug('making a request to the Dad Jokes API')
    response = requests.get('https://icanhazdadjoke.com', headers={"Accept": "text/plain"})
    return response.content


@app.route('/dad-joke-internal')
def dad_joke_internal():
    other_service_url = "https://rbc-devops-sample-dev.azurewebsites.net/dad-joke"
    app.logger.info('Calling the other service')
    response = requests.get(other_service_url)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
