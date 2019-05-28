from flask import Blueprint, jsonify


assignments_page = Blueprint('assignments_page', __name__)

#Gets the test assignment data for given student name
#Name format should be: lastName%20firstName'%20gradyear
@assignments_page.route('/get/testdata/<student_name>/', methods=['GET'])
def get_data(student_name):
    get = mongo.db.data.find_one_or_404({"student_name": student_name}) #finds that instance of the student in the db, returns 404 if not found
    get.pop('_id', None) #removes the id object, only needed for storage purposes
    return jsonify(get) #encodes it into a JSON and returns it