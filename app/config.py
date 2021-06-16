# import os
# from threading import Thread
# import json
#
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text
#
# from .db import database
# from .logging import logging
#
# global TASK
#
# app = Flask(__name__)
#
# HOST = os.environ.get("HOST")
# PORT = os.environ.get("PORT")
#
# log = logging.getLogger(__name__)
#
# TASK = None
#
#
# @app.route('/')
# def index():
#     return 'Hello World!!!'
#
#
# @app.route('/add')
# def add():
#     from app import updateDB
#
#     if os.environ.get('TASK') is None:
#         TASK = Thread(target=updateDB)
#
#     if TASK.is_alive():
#         return 'DataBase Updating ...'
#     else:
#         TASK.start()
#         return 'DataBase Update Started !'
#
#
# @app.route('/newsdata')
# def get_newsdata():
#     newsdata = database.child("Newsdata").get().val()
#     output = []
#     for news in newsdata:
#         if news:
#             output.append(news)
#     output.sort(key=lambda k: k['date'], reverse=True)
#     return {"NewsData": output}
#
#
# @app.route('/recent')
# def get_recentdata():
#     newsdata = database.child("Newsdata").get().val()
#     output = []
#     for news in newsdata:
#         if news:
#             if news['recent']:
#                 output.append(news)
#     output.sort(key=lambda k: k['date'], reverse=True)
#     return {"NewsData": output}
#
#
# if __name__ == '__main__':
#     app.run(host=HOST, port=PORT)
