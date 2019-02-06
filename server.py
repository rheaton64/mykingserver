import os

from flask import Flask
from flask_pymongo import PyMongo
app = Flask(__name__)

os.environ['FLASK_DEBUG'] = "1" # DO NOT USE IN PRODUCTION

@app.route('/hello/')
def hello():
    return "Hello World!"

@app.route('/user/<username>')
def showUsername(username):
    return username

if __name__ == '__main__':
    app.run()