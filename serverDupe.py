import os
import csv

from flask import Flask, jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test_king"
os.environ['FLASK_DEBUG'] = "1" # DO NOT USE IN PRODUCTION
mongo = PyMongo(app)

# returns a list of assignments that match the student token
@app.route('/<token>/assignments/')
def getAssignments(token):
    return token

@app.route('/get/testdata/<student_name>/', methods=['GET'])
def get_data(student_name):
    print(student_name)
    #student_name = student_name.replace('%20', ' ')
    get = mongo.db.data.find_one_or_404({"student_name": student_name})
    get.pop('_id', None)
    return jsonify(get)

# returns a list of classes that match the student token
@app.route('/<token>/classes/')
def getClasses(token):
    return token

# returns a schedule that matches the student token
@app.route('/<token>/schedule/')
def getSchedule(token):
    return token

# returns all current active announcements
@app.route('/announcements/')
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

class Assignment:
    
    def __init__(self, className, assType, assName,dateAss, weekdayDue):
        self.className = className
        self.assType = assType
        self.assName = assName
        self.dateAss = dateAss
        self.weekdayDue = weekdayDue

    def __str__(self):
        return "Class: " + self.className + " , Type: " + self.assType + " , Name: " + self.assName + " , Assign Date: " + self.dateAss + " , Due Date: " + str(self.weekdayDue)
    
    def toString(self):
        return self.className + ',,'+ self.assType + ',,' + self.assName + ',,' + self.dateAss + ',,' + str(self.weekdayDue)

@app.route('/testdata/')
def test():
    print('made it here')
    path = '/Users/rheaton/Desktop/Xcode/mykingserver/data/'
    compileData(path, 'ass')
    return None

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

# literally just declaring a bunch of variables fo use in the future
# if you enjoy the names, thank you, I did too, "assignments" have a conveniently fun abbreviation
sunAss = []
monAss = []
tueAss = []
wedAss = []
thuAss = []
friAss = []
satAss = []
assForDay = [sunAss, monAss, tueAss, wedAss, thuAss, friAss, satAss]

# compiles data, may or may not be needed
def compileData(path, type):
    if type == "sch":
        return None
    if type == "ass":
        name = ""
        numAss = 0
        week = ""
        
        for filename in os.listdir(path):
            for a in assForDay:
                del a[:]
            print(filename)
            # now this is where the magic happens
            # if you don't understand how this works, just google it, using the python "csv" library
            if(filename != ".DS_Store"):
                with open(path + filename) as csv_file:
                    print("im here")
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                    # first row, splitting it into an array of strings and pulling out the week because I'm too lazy to use substring
                        if line_count == 0:
                            splitStr = row[0].split()
                            week = splitStr[8]
                    # third row, holds the student name in there somewhere, pulling it out for future use
                        if line_count == 2:
                            name = row[0]
                    # fourth row is the fun part, this has all the assingments held in it
                    # The all have a bunch of different attributes that I am maticulously extracting and placing into an object
                    # this object will be infinitely easier to use than the existing clump of string
                    # ironic that I'm turning it right back into a clump of string later on, but such is life
                        if line_count == 3:
                        # if you're smart, you've already realized that "day" is a counter that keeps track of the working weekday
                            day = 0
                            for index in row:
                                arr = index.split("\n")
                                if len(arr) > 1:
                                    parseAssignments(0, arr.index('', 4), arr, day)
                                day += 1
                    #else:
                        #print(row)
                        line_count += 1

                # turn each assignment into an assignemnt object, and look up python objects
                # this way they can actually be properly organized and all that fun stuff
                #organized like this:
                # class, assType, assName, assDesc, dateAss, weekDayDue
                # then, in the post, order them in that order with a string delimited by a ",,"

                post = {
                    "student_name": name,
                    "date": week,
                    "number_of_assignments": numAss,
                    "assignmnets": assForDay
                }
                posts = mongo.db.data
                posts.insert_one(post)

def parseAssignments(startIndex, endIndex, arr, day):
    lenSect = endIndex - startIndex
    if lenSect < 5:
        assign = Assignment(arr[startIndex], "ERROR", "INVALID_DATA", "", day)
    else:
        if lenSect > 5:
            arr.pop(endIndex - 4)
            endIndex -= 1
        assign = Assignment(arr[startIndex], arr[startIndex+1], arr[startIndex+2], arr[endIndex-1], day)
    assForDay[day].append(assign.toString())
    if endIndex+1 != len(arr):
        parseAssignments(endIndex+1, arr.index('', endIndex+4), arr, day)

if __name__ == '__main__':
    app.run()