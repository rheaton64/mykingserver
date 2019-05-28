from flask_pymongo import PyMongo

mongo = None

def init(app):
    global mongo
    print("app init")
    mongo = PyMongo(app)