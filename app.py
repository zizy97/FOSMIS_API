import os
import os

HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!!!'


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
