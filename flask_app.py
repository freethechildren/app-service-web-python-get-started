import logging
import os
import time
import requests

from flask import Flask, Response

app = Flask(__name__)


@app.route('/')
def hello_world():
    logging.error('Testing error logging...')
    return 'Hello, World!'


@app.route('/snail')
def slow():
    logging.warning('This API is sooooo slow!!!')
    time.sleep(5)
    logging.info('making an API request to ')
    return "I'm ALIVE!"


@app.route('/dad-joke')
def dad_joke():
    logging.debug('making a request to the Dad Jokes API')
    response = requests.get('https://icanhazdadjoke.com')
    return response.content


@app.route('/500')
def five_hundred():
    logging.error('Oops! Something went wrong :)')
    return Response(status=500)


@app.route('/403')
def four_oh_one():
    logging.warning('This guy is not authorized to access. WATCH HIM!')
    return Response(status=401)


# is PORT env var passed by the App Service?
PORT = os.getenv('PORT', 80)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
