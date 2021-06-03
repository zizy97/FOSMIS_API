import os
from threading import Thread

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .logging import logging

app = Flask(__name__)

HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

log = logging.getLogger(__name__)

# DATABASE_URL=os.environ.get("DATABASE_URL","sqlite:///sample.db")
DATABASE_URL = 'sqlite:///sample.db'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)


class NewsData(db.Model):
    __tablename__ = 'newsdata'
    id = db.Column(db.VARCHAR(3), primary_key=True)
    date = db.Column(db.VARCHAR(20))
    content = db.Column(db.String)
    description = db.Column(db.TEXT)
    path = db.Column(db.String)

    def __init__(self, id, date, content, description, path):
        self.id = id
        self.date = date
        self.content = content
        self.description = description
        self.path = path

    def __repr__(self):
        return f"id-{self.id} date-{self.date} content-{self.content} description-{self.description} path-{self.path}"

TASK = None


@app.route('/')
def index():
    return 'Hello World!!!'


@app.route('/add')
def add():
    global TASK
    from app import updateDB

    if TASK is None:
        TASK = Thread(target=updateDB)

    if TASK.isAlive():
        return 'DataBase Updating ...'
    else:
        TASK.start()
        return 'DataBase Update Started !'


@app.route('/createdb')
def createdb():
    db.create_all()
    return "Db created!!!"


@app.route('/newsdata')
def get_newsdata():
    newsdata = NewsData.query.all()
    output = []
    for news in newsdata:
        log.info(news)
        data = {"ID": news.id, "DATE": news.date, "CONTENT": news.content,
                "DESCRIPTION": news.description, "PATH": news.path}
        output.append(data)
    return {"NewsData": output}


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
