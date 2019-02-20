import os
import csv

from flask import Flask
from flask_pymongo import PyMongo
from flask import request
app = Flask(__name__)

os.environ['FLASK_DEBUG'] = "1" # DO NOT USE IN PRODUCTION

# returns a list of assignments that match the student token
@app.route('/<token>/assignments/', method = ['GET'])
def getAssignments(token):
    return token

# returns a list of classes that match the student token
@app.route('/<token>/classes/', methods = ['GET'])
def getClasses(token):
    return token

# returns a schedule that matches the student token
@app.route('/<token>/schedule/', methods = ['GET'])
def getSchedule(token):
    return token

# returns all current active announcements
@app.route('/announcements/', methods = ['GET'])
def getAnnouncements():
    return "Hello"

# called when a valid token wants tp:
# GET: See all their announcements that they have posted
# POST: Update / Edit one of the announcements
# PUT: Add a new announcement
@app.route('/announcements/<token>/<value>', methods = ['GET', 'POST', 'PUT'])
def announce(token, value):
    if request.method == 'GET':
       getAnnouncementsFromToken(token)
    if request.method == 'POST':
        updateAnnouncement(token, value)
    else:
        addAnnouncement(token, value)

# Gets all announcements accessible from a token
def getAnnouncementsFromToken(token):
    return None

# updates announement, given token for credentials and value for data 
def updateAnnouncement(token, value):
    return None

# adds a new announcements, given token for credentials and value for data
def addAnnouncement(token, value):
    return None

# return the letter dat based on the calendar day
def getDay():
    return None

# reHashes a token back into a student ID
def getIDFromToken(token):
    return token

# compiles data, may or may not be needed
def compileData(filepath, type):
    if type == "sch":
        return None
    if type == "ass":
        with open('filepath', mode = 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            return None # finish this, working on it in another file



if __name__ == '__main__':
    app.run()