from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
import bcrypt
import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'

db = sqlalchemy.SQLAlchemy(app)

class PotentialTAs(db.Model):#Table containing basic TA information gathered at sign-up
    
    email = db.Column(db.String(64), nullable=False)
    firstName = db.Column(db.String(64), nullable=False)
    lastName = db.Column(db.String(64), nullable=False)
    gpa = db.Column(db.Float, nullable=False)
    gradDate = db.Column(db.String, nullable=False)
    
    # TODO 1: add all of the columns for the other table attributes

def row_to_obj_potential_ta(row):
    row = {
            "id": row.id,
            "loginHash": row.loginHash,
            "email": row.email,
            "firstName": row.firstName,
            "lastName": row.lastName,
            "gpa": row.gpa,
            "gradDate": row.gradDate
        }
    return row

class TAs(db.Model):#taIdentifier is PotentialTAs.id, classForApp id ClassesForApp.id
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    loginHash = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(64)), nullable=False)
    firstName = db.Column(db.String(64)), nullable=False)
    lastName = db.Column(db.String(64)), nullable=False)
    phone = db.Column(db.String(64)) 
    major = db.Column(db.String(64))
    cum_gpa = db.Column(db.Float)
    expected_grad = db.Column(db.String)
    prev_TA = db.Column(db.Boolean)#Previously a TA?
    salt = db.Column(db.String)

class TAApplications(db.Model):#Table containing course specific info gathered at apply
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    taIdentifier = db.Column(db.Integer, secondary_key=True, nullable=False)#id in PotentialTAs Table
    course_num = db.Column(db.String, nullable=False)
    gradeInClass = db.Column(db.String, nullable=False)
    sem_apply = db.Column(db.String, nullable=False)
    sem_taken = db.Column(db.String, nullable=False)
    course_TA = db.Column(db.Boolean, nullable=False)#Previously a TA in this course?

class Professors(db.Model):
    id = db.Column(db.String, primary_key=true, nullable=False)#is email
    loginHash = db.Column(db.Integer, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.String, nullable=False)

    def __init__(self, id, loginHash, firstName, lastName, salt):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.loginHash = loginHash
        self.salt = salt

class ClassesForApp(db.Model):
    id = db.Column(db.String), primary_key=True, nullable=False)
    profIdentifier = db.Column(db.Integer, secondary_key=True, nullable=False)
    subject = db.Column(db.String(10), nullable=False)
    courseNumber = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1024)), nullable=False)
    sections = db.Column(db.Integer, nullable =False)

base_url = '/api/'


def row_to_obj_prof(row):
    row = {
        "id" : row.id
        "loginHash":row.loginHash
        "email":row.email
        "firstName":firstName
        "lastName":lastName
    }
    return row

def row_to_obj_prof_secure(row):
    row = {
        "id" : row.id
        "email":row.email
        "firstName":firstName
        "lastName":lastName
    }
    return row

@app.route(base_url+'createProf',methods=["POST"])
def createProf():
    json = request.get_json()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(json[password], salt)
    prof = Professors(json[email], hashed, json[firstName], json[lastName], salt)
    db.session.add(prof)
    db.session.commit()
    db.session.refresh(prof)
    return jsonify({"status":1,"professor":row_to_obj_prof_secure(prof)}), 200

base_url = '/api/'

  
def main():
    db.create_all() # creates the tables you've provided
    app.run()       # runs the Flask application  

if __name__ == '__main__':
    main()
