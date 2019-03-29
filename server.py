import os
import csv

from flask import Flask, jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DBNAME'] = 'test_king'
app.config['MONGO_USERNAME'] = 'studentAdmin'
app.config['MONGO_PASSWORD'] = 'longlivetheking'
app.config['MONGO_AUTH_SOURCE'] = 'admin'
app.config["MONGO_URI"] = "mongodb://studentAdmin:longlivetheking@localhost:27017/test_king?authSource=admin"
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

@app.route('/get/testsch/<student_name>/', methods=['GET'])
def get_sch(student_name):
    get = mongo.db.sch.find_one_or_404({"student_name": student_name})
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

class Class:

    def __init__(self, color, className, teacher, roomNum):
        self.color = color
        self.className = className
        self.teacher = teacher
        self.roomNum = roomNum

    def toString(self):
        return self.color + ",," + self.className + ",," + self.teacher + ",," + self.roomNum


@app.route('/testdata/parseass')
def test():
    print('made it here')
    path = '/home/student/data/'
    compileData(path, 'ass')
    return None

@app.route('/testdata/parsesch')
def sche():
    path = '/home/student/data/sch/'
    compileData(path, 'sch')
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

aSch = []
bSch = []
cSch = []
dSch = []
eSch = []
fSch = []
gSch= []
hSch = []
schedule = [aSch, bSch, cSch, dSch, eSch, fSch, gSch, hSch]

# compiles data, may or may not be needed
def compileData(path, type):
    if type == "sch":
        name = ""
        for a in schedule:
                del a[:]
        for filename in os.listdir(path):
            with open(path + filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                start_index = 0
                working_row = ""
                finished = 0
                for row in csv_reader:
                    if line_count % 2 == 0:
                        print("here")
                        print(row)
                        if line_count == 2:
                            if row[1] == "A\n":
                                start_index = 0
                            if row[1] == "B\n":
                                start_index = 1
                            if row[1] == "C\n":
                                start_index = 2
                            if row[1] == "D\n":
                                start_index = 3
                            if row[1] == "E\n":
                                start_index = 4
                            if row[1] == "F\n":
                                start_index = 5
                            if row[1] == "G\n":
                                start_index = 6
                            if row[1] == "H\n":
                                start_index = 7
                            working_row = row[1]
                            print(start_index)
                        if line_count >= 2 and row[1] != working_row:
                            #print("Working Row: " + working_row)
                            start_index += 1
                            if start_index == 8:
                                start_index = 0
                            working_row = row[1]
                            #print(start_index)
                            finished += 1
                        if finished == 8:
                            break
                        if line_count >= 2 and row[8] != "Attendance":
                            if name == "":
                                name = row[3]
                            schedule[start_index].append(parseClass(row))
                    line_count += 1
                post = {
                    "student_name": name,
                    "schedule": schedule
                }
                posts = mongo.db.sch
                posts.insert_one(post)
    if type == "ass":
        name = ""
        numAss = 0
        week = ""
        
        for filename in os.listdir(path):
            print(filename)
            for a in assForDay:
                del a[:]
            # now this is where the magic happens
            # if you don't understand how this works, just google it, using the python "csv" library
            with open(path + filename) as csv_file:
                print("im here")
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    print(str(line_count) + ": " + str(row))
                # first row, splitting it into an array of strings and pulling out the week because I'm too lazy to use substring
                    if line_count == 0:
                        splitStr = row[0].split()
                        week = splitStr[8]
                # third row, holds the student name in there somewhere, pulling it out for future use
                    if line_count == 4:
                        name = row[0]
                # fourth row is the fun part, this has all the assingments held in it
                # The all have a bunch of different attributes that I am maticulously extracting and placing into an object
                # this object will be infinitely easier to use than the existing clump of string
                # ironic that I'm turning it right back into a clump of string later on, but such is life
                    if line_count == 6:
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

def parseClass(row):
    #getting color
    if row[8] != "Yellow":
        tempColor = row[8][:row[8].find(" ")]
    else:
        tempColor = row[8]
    #getting class name
    tempName = row[4][:len(row[4])-4]
    #getting teacher name
    tempTeach = row[9][:len(row[9])-1]
    #getting room number
    tempNum = str(row[7][len(row[7])-3:len(row[7])])
    #making object and inserting into array
    newClass = Class(tempColor, tempName, tempTeach, tempNum)
    return newClass.toString()

if __name__ == '__main__':
    app.run()