import json
from db import db
from flask import Flask, request
from db import Course, Assignment, User
import os #module to access env variables

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# your routes here
@app.route("/")
def greeting(): 
    return f"hello {os.environ['NAME']} {os.environ['NETID']}" #github will not see this unless u push env file!!! 
#but can load env file to docker-compose bc we need it for the docker image!!!

@app.route("/api/courses/", methods = ["GET"])
def get_courses():
    """
    Endpoint for getting all courses
    """
    courses = [course.serialize() for course in Course.query.all()]
    return success_response ({"courses": courses}) 

@app.route("/api/courses/", methods = ["POST"])
def create_course():
    """
    Endpoint for creating a new course
    """
    body = json.loads(request.data)
    #initialize task
    if body.get("code") == None or body.get("name") == None:
        return failure_response("Missing field in request", 400)
    new_course = Course(
        code = body.get("code"),
        name = body.get("name")
    )
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)

@app.route("/api/courses/<int:id>/", methods = ["GET"])
def get_course(id):
    """
    Endpoint for getting a course by id
    """
    course = Course.query.filter_by(id = id).first()
    if course is None: 
        return failure_response("Course not found")
    return success_response(course.serialize())

@app.route("/api/courses/<int:id>/", methods = ["DELETE"])
def delete_course(id):
    """
    Endpoint for deleting a course by id
    """
    course = Course.query.filter_by(id = id).first()
    if course is None: 
        return failure_response("Course not found")
    db.session.delete(course)
    db.session.commit()
    return success_response (course.serialize())

@app.route("/api/users/", methods = ["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """
    body = json.loads(request.data)
    #initialize task
    if body.get("name") == None or body.get("netid") == None:
        return failure_response("Missing field in request", 400)
    new_user = User(
        name = body.get("name"),
        netid = body.get("netid"),
    )
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/api/users/<int:id>/", methods = ["GET"])
def get_user(id):
    """
    Endpoint for getting a user by id
    """
    user = User.query.filter_by(id = id).first()
    if user is None: 
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/api/courses/<int:id>/add/", methods = ["POST"])
def add_user_to_course(id):
    """
    Endpoint for adding a user to course indicated by id
    """
    #get user by its id 
    #check if it;s none
    body = json.loads(request.data)
    user_id = body.get("user_id")
    type = body.get("type")
    if user_id == None or type == None:
        return failure_response("Missing field in request", 400)
    user = User.query.filter_by(id = user_id).first()
    #get course specified by id:
    course = Course.query.filter_by(id=id).first()
    if user is None: 
        return failure_response("User not found")
    if course is None:
        return failure_response("Course not found")
    
    if type == "student":
        #add to course specified by id 
        course.students.append(user)
        db.session.commit()
        return success_response(course.serialize())
        
    if type == "instructor":
        #add to course specified by id 
        course.instructors.append(user)
        db.session.commit()
        return success_response(course.serialize())
    
@app.route("/api/courses/<int:id>/assignment/", methods = ["POST"])
def create_assignment(id):
    """
    Endpoint for creating an assignment
    """
    course = Course.query.filter_by(id = id).first()
    if course is None: 
        return failure_response("Course not found")
    body = json.loads(request.data)
    if body.get("title") == None or body.get("due_date") == None:
        return failure_response("Missing field in request body", 400)
    new_assignment = Assignment (
        title = body.get("title"),
        due_date = body.get("due_date"),
        course_id = id,)
    db.session.add(new_assignment)
    db.session.commit()
    return success_response(new_assignment.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
