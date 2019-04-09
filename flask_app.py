import logging
import os
import time

import requests
from applicationinsights.flask.ext import AppInsights
from flask import Flask, Response

INSTRUMENTATION_KEY = '115fcb01-ff5c-42db-9b69-5e6ae017f9a7'

# instantiate the Flask application
app = Flask(__name__)
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = INSTRUMENTATION_KEY

# log requests, traces and exceptions to the Application Insights service
appinsights = AppInsights(app)
appinsights.context.device.role_name = 'poulad-role'


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


# is PORT env var passed by the App Service?
PORT = os.getenv('PORT', 80)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
