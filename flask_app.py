import logging
import os

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    logging.error('Testing error logging...')
    return 'Hello, World!'


PORT = os.getenv('PORT', 5000)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
