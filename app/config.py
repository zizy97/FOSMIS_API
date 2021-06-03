import os
from threading import Thread
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .logging import logging

global TASK

app = Flask(__name__)

HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

log = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL",
                              "postgres://tknjoyeqxelpva"
                              ":0d8e055962b328ed8d86bbc8762f3df74f63af6d5b4cb95e53c832dcc13133a1@ec2-34-202-54-225"
                              ".compute-1.amazonaws.com:5432/d8mktjur1o1vuf")

# DATABASE_URL = 'sqlite:///sample.db'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy(app)


class Source:
    def __init__(self, webviewlink, webcontentlink):
        self.webviewlink = webviewlink
        self.webcontentlink = webcontentlink

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class NewsData(db.Model):
    __tablename__ = 'newsdata'
    id = db.Column(db.INT, primary_key=True)
    date = db.Column(db.TIMESTAMP)
    title = db.Column(db.String)
    description = db.Column(db.TEXT)
    path = db.Column(db.PickleType)
    recent = db.Column(db.BOOLEAN)

    def __init__(self, id, date, title, description, path, recent):
        self.id = id
        self.date = date
        self.title = title
        self.description = description
        self.path = path
        self.recent = recent

    def __repr__(self):
        return f"id-{self.id} date-{self.date} title-{self.title} description-{self.description} path-{self.path.toJSON()} recent-{self.recent} "


TASK = None


@app.route('/')
def index():
    return 'Hello World!!!'


@app.route('/add')
def add():
    from app import updateDB

    if os.environ.get('TASK') is None:
        TASK = Thread(target=updateDB)

    if TASK.is_alive():
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
        if news.path:
            # data = {"ID": news.id, "DATE": news.date, "CONTENT": news.content,
            #         "DESCRIPTION": news.description, "SOURCE": news.path.toJSON()}
            data = {"ID": news.id, "DATE": news.date, "TITLE": news.title,
                    "DESCRIPTION": news.description, "SOURCE": [news.path.webviewlink, news.path.webcontentlink],
                    "RECENT": news.recent}
        else:
            data = {"ID": news.id, "DATE": news.date, "TITLE": news.title,
                    "DESCRIPTION": news.description, "SOURCE": None, "RECENT": news.recent}
        output.append(data)
    return {"NewsData": output}


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
