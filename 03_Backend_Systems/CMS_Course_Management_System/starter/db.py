from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#We need two assoc tables - one for students and one for instructorrs
student_course_assoc = db.Table (
    "student_course_assoc",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("student_id", db.Integer, db.ForeignKey("user.id")))

instructor_course_assoc = db.Table (
    "instructor_course_assoc",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("instructor_id", db.Integer, db.ForeignKey("user.id")))

# your classes here
class Course(db.Model):
    """
    Course Model
    """
    __tablename__ = "course" 
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    code = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    assignments = db.relationship("Assignment", cascade="delete")
    instructors = db.relationship(
         "User", secondary = instructor_course_assoc, back_populates = "instructor_courses")
    students = db.relationship(
         "User", secondary = student_course_assoc, back_populates = "student_courses")

    def __init__ (self, **kwargs):
        """
        Initialize a Course Object
        """
        self.code=kwargs.get("code", "")
        self.name = kwargs.get("name", "")

    def serialize(self):
        return {
            "id": self.id,
            "code": self.code, 
            "name": self.name,
            "assignments": [s.simple_serialize() for s in self.assignments],
            "instructors": [c.simple_serialize() for c in self.instructors],
            "students": [s.simple_serialize() for s in self.students]
        }
    def simple_serialize(self):
         return {
            "id": self.id,
            "code": self.code, 
            "name": self.name,
         }
    
class User(db.Model):
    """
    User Model
    """
    __tablename__ = "user" 
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)
    instructor_courses = db.relationship("Course", secondary=instructor_course_assoc, back_populates="instructors")
    student_courses = db.relationship("Course", secondary=student_course_assoc, back_populates="students")

    def __init__ (self, **kwargs):
        """
        Initialize a User Object
        """
        self.name=kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")
    
    def serialize(self):

            return {
                "id": self.id,
                "netid": self.netid,
                "name": self.name,
                "courses": 
                [c.simple_serialize() for c in self.instructor_courses] + 
                ([c.simple_serialize() for c in self.student_courses]),
            }
        
    
    def simple_serialize(self):
            """
            Serialize a user object without courses field!
            """
            return {
                    "id": self.id,
                    "netid": self.netid,
                    "name": self.name,
                }
           

    
class Assignment(db.Model):
    """
    Assignment Model
    """
    __tablename__ = "assignment" 
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String, nullable = False)
    due_date = db.Column(db.Integer, nullable = False)
    #referencing one unique key 
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    

    def __init__(self, **kwargs):
        """
        Initialize a subtask object
        """
        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date", 0)
        self.course_id =kwargs.get("course_id", 0)
        

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title, 
            "due_date": self.due_date,
            "course": Course.query.filter_by(id = self.course_id).first().simple_serialize()
        }
    
    def simple_serialize(self):
         """
         Serialize assignment - no course field
         """
         return {"id": self.id, 
                 "title": self.title,
                 "due_date": self.due_date
                 }
