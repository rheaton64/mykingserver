import os
import csv
import datetime

from flask import Flask, jsonify, flash, render_template
from flask import request
from flask_pymongo import PyMongo


#from endpoints.assignments import assignments_page

#The absolute motherload of code, the big kahuna, the behemoth
#MyKingApp backend dataserver
#Everything is here is needed for the app to function properly, and it all has a function, even though it might not seem like it
#Uses Flask, a webserver microframework, as well as Flask-PyMongo to interface with the MongoDB server on the same machine
#Current port used: 5000
#Current Mongo port: 27017
#Written by Ryan Heaton, 2019

#Sets up the config for interface with MongoDB
#Not sure which of these are actually necessary, but keeping them nonetheless
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

#app.register_blueprint(assignments_page, url_prefix='/assignments')

#Returns a list of assignments that match the student token
#Currently WIP, use testdata for now
@app.route('/<token>/assignments/')
def getAssignments(token):
    return token

#Gets the test assignment data for given student name
#Name format should be: lastName%20firstName'%20gradyear
@app.route('/get/testdata/<student_name>/', methods=['GET'])
def get_data(student_name):
    get = mongo.db.data.find_one_or_404({"student_name": student_name}) #finds that instance of the student in the db, returns 404 if not found
    get.pop('_id', None) #removes the id object, only needed for storage purposes
    return jsonify(get) #encodes it into a JSON and returns it

#Does the same as above, but fo schedule instead of assignments
@app.route('/get/testsch/<student_name>/', methods=['GET'])
def get_sch(student_name):
    get = mongo.db.sch.find_one_or_404({"student_name": student_name})
    get.pop('_id', None)
    return jsonify(get)

#Returns a list of classes that match the student token
#Currently WIP
@app.route('/<token>/classes/')
def getClasses(token):
    return token

#Returns a schedule that matches the student token
#Currenty WIP, use testsch for now
@app.route('/<token>/schedule/')
def getSchedule(token):
    return token

#Returns all current active announcements
#Currently WIP, I have no idea when it will actually work
@app.route('/announcements/')
def getAnnouncements():
    return "Hello"

#Called when a valid token wants to post:
#GET: See all their announcements that they have posted
#POST: Post a new announcement
#Currently WIP, might never be implemented, who knows
#TODO: this right here
@app.route('/announcements/<token>/', methods = ['GET', 'POST'])
def announce(token):
    if request.method == 'GET':
       getAnnouncementsFromToken(token)
    else:
        json_data = request.form
        return addAnnouncement(token, json_data)

#This is where the fun begins
#This class stores the necessary information for an Assignment object that is used when parsing assignment data
#Parameters: Name of Class, Type of Assignment, Name of Assignment, Date Assigned, Weekday Due
#Used in parseAssignments func
class Assignment:
    
    def __init__(self, className, assType, assName,dateAss, weekdayDue): #just a good old init function
        self.className = className
        self.assType = assType
        self.assName = assName
        self.dateAss = dateAss
        self.weekdayDue = weekdayDue

    def __str__(self): #probably not needed at this point
        return "Class: " + self.className + " , Type: " + self.assType + " , Name: " + self.assName + " , Assign Date: " + self.dateAss + " , Due Date: " + str(self.weekdayDue)
    
    def toString(self): #converts the data in the class to a usable string to post
        return self.className + ',,'+ self.assType + ',,' + self.assName + ',,' + self.dateAss + ',,' + str(self.weekdayDue)

#Very similar to the Assignment class, but this time it stores an individual class for parsing schedule data
#Parameters: Color, Name of Class, Name of Teacher, Room Number
class Class:

    def __init__(self, color, className, teacher, roomNum):#init method
        self.color = color
        self.className = className
        self.teacher = teacher
        self.roomNum = roomNum

    def toString(self):#converts the data in the class to a usable string to post
        return self.color + ",," + self.className + ",," + self.teacher + ",," + self.roomNum

#Route to call when there are new unparsed CSVs that needed to be turned into assignments
#Doesn't return anything, so expect an error, but does a lot of work behind the scenes
#TODO: make it delete the files
@app.route('/testdata/parseass')
def test():
    path = '/home/student/data/'#path at which the files are stored
    compileData(path, 'ass')#calls compile method for ass, does the work, see below
    return None

#Same as above but parses schedule files
#Doesn't return anything, so expect an error, but does a lot of work behind the scenes
#TODO: make it delete the files
@app.route('/testdata/parsesch')
def sche():
    path = '/home/student/data/sch/'#path at which the files are stored
    compileData(path, 'sch')#calls compile method for sch, does the work, see below
    return None

#All these 3 below are for announcements which are currently not implemented
#TODO: All these things and more

# Gets all announcements accessible from a token
def getAnnouncementsFromToken(token):
    return None

# updates announement, given token for credentials and value for data 
def updateAnnouncement(token, value):
    return None

validPosters = ["Heaton", "Creveling"]

@app.route('/announcements/webapp')
def annWeb():
    return render_template('inputAnn.html')

@app.route('/announcements/webapp/result', methods = ['POST', 'GET'])
def annWebResult():
    if request.method == 'POST':
        json_data = request.form
        return addAnnouncement('web_app_token', json_data)

# adds a new announcements, given token for credentials and value for data
def addAnnouncement(token, json_data):
    print(json_data)
    annType = json_data.get('type')
    author = json_data.get('author')
    title = json_data.get('title')
    time = json_data.get('datetime')
    body = json_data.get('body')

    if(token == 'web_app_token'):
        token = json_data.get('token')

    try:
        poster = validPosters.index(token)

        print(str(poster))

        post = {
            "poster": poster,
            "type": annType,
            "author": author,
            "time": time,
            "title": title,
            "body": body
        }

        posts = mongo.db.ann
        posts.insert_one(post)

        return "done"
    except ValueError:
        return "invalid_poster_token"


@app.route('/get/letterday/webapp/')
def getDayApp():
    return render_template('inputDay.html')

@app.route('/get/letterday/webapp/result', methods = ['POST', 'GET'])
def getDayAppResult():
    if request.method == 'POST':
        form_data = request.form
        month = int(form_data.get('Month'))
        day = int(form_data.get('Day'))
        year = int(form_data.get('Year'))

        omit = [datetime.date(2018, 9, 10), datetime.date(2018, 9, 19), datetime.date(2018, 10, 8) #list of days to be omitted, i.e. winter & spring break, thanksgiving, etc.
            , datetime.date(2018, 11, 12), datetime.date(2018, 11, 21), datetime.date(2018, 11, 22), datetime.date(2018, 11, 23)
            , datetime.date(2018, 12, 24), datetime.date(2018, 12, 25), datetime.date(2018, 12, 26), datetime.date(2018, 12, 27), datetime.date(2018, 12, 28)
            , datetime.date(2018, 12, 31), datetime.date(2019, 1, 1), datetime.date(2019, 1, 2), datetime.date(2019, 1, 3), datetime.date(2019, 1, 4)
            , datetime.date(2019, 1, 21), datetime.date(2019, 2, 14), datetime.date(2019, 2, 15), datetime.date(2019, 2, 18)
            , datetime.date(2019, 3, 11), datetime.date(2019, 3, 12), datetime.date(2019, 3, 13), datetime.date(2019, 3, 14), datetime.date(2019, 3, 15)
            , datetime.date(2019, 3, 18), datetime.date(2019, 3, 19), datetime.date(2019, 3, 20), datetime.date(2019, 3, 21), datetime.date(2019, 3, 22)
            , datetime.date(2019, 4, 19), datetime.date(2019, 5, 27)]

        startDate = datetime.date(2018, 9, 6) #first day of school, first A day of the year, the day to count back to

        now = datetime.date(year, month, day) #sets the current date

        deltaDays = now - startDate #finds the delta(change) in days between now and the start date
        days = deltaDays.days #converts the delta into a nice int value

        weekends = days/7.0 #divides the amount of days by 7 to get the amount of weekends

        weekends = round(weekends) #if something breaks, it's one of the rounding lines, this is here only because it fixes counting errors

        days -= 2*weekends #subtracts 2 days per each weekend calculated, because there is no school on weekends

        for d in omit: #for each omitted day that has passed(delta day is greater than zero), it subtracts one day
            if (now-d).days >= 0:
                days -= 1

        days = round(days) #see above, this will be the death of me

        days += 1 #adds one day, I don't even think God knows why this in needed, but it makes everything work

        letterNum = days % 8 #gets the remainder when divided by 8, because the schedule works on an 8 day rotation

        letter = int(letterNum) #converts from double to int, this is needed for the if statements
        letterDay = ""
        #converts corresponding number to letter, starting at 0=A and endingat 7=H
        if(letter == 0):
            letterDay = "A"
        if(letter == 1):
            letterDay = "B"
        if(letter == 2):
            letterDay = "C"
        if(letter == 3):
            letterDay = "D"
        if(letter == 4):
            letterDay = "E"
        if(letter == 5):
            letterDay = "F"
        if(letter == 6):
            letterDay = "G"
        if(letter == 7):
            letterDay = "H"

        return letterDay #returns the letter day of today
#Wow, this took way longer than I want to admit
#This beast of a function returns a simple string (or int, prefence here), that represents the current letter day
#Counts back to the first day of school, omits weekends and break days, and then gives you that beautiful value that corresponds to a letter betweeen A-F (0-7)
#This is finished, DO NOT TOUCH unless you are changing start date or omit days
@app.route('/get/letterday/', methods = ["GET"])
def getDay():
    letterDay = ""

    omit = [datetime.date(2018, 9, 10), datetime.date(2018, 9, 19), datetime.date(2018, 10, 8) #list of days to be omitted, i.e. winter & spring break, thanksgiving, etc.
            , datetime.date(2018, 11, 12), datetime.date(2018, 11, 21), datetime.date(2018, 11, 22), datetime.date(2018, 11, 23)
            , datetime.date(2018, 12, 24), datetime.date(2018, 12, 25), datetime.date(2018, 12, 26), datetime.date(2018, 12, 27), datetime.date(2018, 12, 28)
            , datetime.date(2018, 12, 31), datetime.date(2019, 1, 1), datetime.date(2019, 1, 2), datetime.date(2019, 1, 3), datetime.date(2019, 1, 4)
            , datetime.date(2019, 1, 21), datetime.date(2019, 2, 14), datetime.date(2019, 2, 15), datetime.date(2019, 2, 18)
            , datetime.date(2019, 3, 11), datetime.date(2019, 3, 12), datetime.date(2019, 3, 13), datetime.date(2019, 3, 14), datetime.date(2019, 3, 15)
            , datetime.date(2019, 3, 18), datetime.date(2019, 3, 19), datetime.date(2019, 3, 20), datetime.date(2019, 3, 21), datetime.date(2019, 3, 22)
            , datetime.date(2019, 4, 19), datetime.date(2019, 5, 27)]

    startDate = datetime.date(2018, 9, 6) #first day of school, first A day of the year, the day to count back to

    now = datetime.datetime.now() #sets the current date

    if(now.weekday() == 5 or now.weekday() == 6):
        letterDay = "W"
    else:
        deltaDays = now.date() - startDate #finds the delta(change) in days between now and the start date
        days = deltaDays.days #converts the delta into a nice int value

        weekends = days/7.0 #divides the amount of days by 7 to get the amount of weekends

        weekends = round(weekends) #if something breaks, it's one of the rounding lines, this is here only because it fixes counting errors

        days -= 2*weekends #subtracts 2 days per each weekend calculated, because there is no school on weekends

        for d in omit: #for each omitted day that has passed(delta day is greater than zero), it subtracts one day
            if (now.date()-d).days >= 0:
                days -= 1

        days = round(days) #see above, this will be the death of me

        days += 1 #adds one day, I don't even think God knows why this in needed, but it makes everything work

        letterNum = days % 8 #gets the remainder when divided by 8, because the schedule works on an 8 day rotation

        letter = int(letterNum) #converts from double to int, this is needed for the if statements
        #converts corresponding number to letter, starting at 0=A and endingat 7=H
        if(letter == 0):
            letterDay = "A"
        if(letter == 1):
            letterDay = "B"
        if(letter == 2):
            letterDay = "C"
        if(letter == 3):
            letterDay = "D"
        if(letter == 4):
            letterDay = "E"
        if(letter == 5):
            letterDay = "F"
        if(letter == 6):
            letterDay = "G"
        if(letter == 7):
            letterDay = "H"

    output = {
        "letter": letterDay
    } 
    
    return jsonify(output) #returns the letter day of today

#ReHashes a token back into a student ID
#I am not looking forward to inplementing this, I may never, who knows
#TODO: hopefully not this
def getIDFromToken(token):
    return token

#Literally just declaring a bunch of variables foR use in the future
#If you enjoy the names, thank you, I did too, "assignments" have a conveniently fun abbreviation
#Stores assignements data some nested arrays
sunAss = []
monAss = []
tueAss = []
wedAss = []
thuAss = []
friAss = []
satAss = []
assForDay = [sunAss, monAss, tueAss, wedAss, thuAss, friAss, satAss]

#Similar to above, stores schedule data in nested arrays
aSch = []
bSch = []
cSch = []
dSch = []
eSch = []
fSch = []
gSch= []
hSch = []
lunchTimes = [True, True, True, True, True, True, True, True]
schedule = [aSch, bSch, cSch, dSch, eSch, fSch, gSch, hSch]

#The Big Daddy of all fun data compiling methods
#Takes in the path of the folder, and the type of data in the folder, then eats it all up and spits it out into the MongoDB
#Type can either be "ass" for assignments or "sch" for schedules
def compileData(path, type):
    if type == "sch": #if you're dealing with a schedule
        for filename in os.listdir(path): #goes through each file in the folder
            for a in schedule: #clears the list that stores the data
                del a[:]
            name = ""
            lunchTimes = [True, True, True, True, True, True, True, True]
            with open(path + filename) as csv_file: #opens the csvs
                csv_reader = csv.reader(csv_file, delimiter=',') #creates the csv reader
                #V A R I A B L E S
                line_count = 0
                start_index = 0
                working_row = ""
                finished = 0
                for row in csv_reader: #goes through each row
                    #So basically there's a tiny issue where csv's are read differently on the server than they are here
                    #All of the lines are followed by blanks lines when run remotely, so that means we only read the lines that are even numbered
                    #It is embarrasing to say that I spent way too much time on this stuff before I realized the error
                    if line_count % 2 == 0:
                        if line_count == 2: #figures out the first letter day shown
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
                            working_row = row[1] #sets the first working row
                            #All of the following code, up till break, has to do with switching the working row
                            #It's pretty self explanatory
                        if line_count >= 2 and row[1] != working_row:
                            start_index += 1
                            if start_index == 8:
                                start_index = 0
                            working_row = row[1]
                            finished += 1
                        if finished == 8:
                            break
                        if line_count >= 2 and row[8] != "Attendance": #sets the name
                            if name == "":
                                name = row[3]
                            print(row[5])
                            schedule[start_index].append(parseClass(row)) #parses that beautiful data, see parseClass method
                            if row[5] == "11:30 AM" or row[5] == "12:00 PM":
                                lunchTimes[start_index] = isFirstLunch(row)
                    line_count += 1
                #This creates the post that uploads the schedule to the server
                #The "schedule is organized as an array of arrays"
                #Each subarray corresponds to a letter day (indexes 0-7)
                #Each subarray contains "Class" object strings that hold all the data we need
                post = {
                    "student_name": name, #string for student name
                    "schedule": schedule, #array of arrays for classes
                    "isFirstLunch": lunchTimes
                }
                posts = mongo.db.sch #uploads to "sch"
                posts.insert_one(post)

    if type == "ass": #if you're dealing with assignments
        #V A R I A B L E S
        name = ""
        numAss = 0
        week = ""
        
        for filename in os.listdir(path):
            print(filename)
            for a in assForDay:#clears array for fun and good stuff
                del a[:]
            #Now this is where the magic happens
            #If you don't understand how this works, just google it, using the python "csv" library
            with open(path + filename) as csv_file:
                print("im here")
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:#goes through each row
                #First row, splitting it into an array of strings and pulling out the week because I'm too lazy to use substring
                    if line_count == 0:
                        splitStr = row[0].split()
                        week = splitStr[8]
                #Third row, holds the student name in there somewhere, pulling it out for future use
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
                                parseAssignments(0, arr.index('', 4), arr, day) #parses, but assignments this time. See the method for more details
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
                "number_of_assignments": numAss,# doesn't work right now because I'm lazy
                "assignments": assForDay
            }
            posts = mongo.db.data #uploads to "data"
            posts.insert_one(post)

#I really don't wanna explain this one, it's pretty self explanatory if you look at it
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
    if row[8] != "Yellow": #for some reason yellow period is not working well, so I'm making a fun exception
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

def isFirstLunch(row):
    if row[5] == "11:30 AM":
        return False
    return True

if __name__ == '__main__':
    app.run()