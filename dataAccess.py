from __main__ import app
from flask import Flask, jsonify, request
import flask_sqlalchemy as sqlalchemy
import bcrypt, datetime, sys, uuid
db = sqlalchemy.SQLAlchemy(app)

class Professors(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False)#is wsu id
    loginHash = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    salt = db.Column(db.String, nullable=False)


    def __init__(self, request):
        json = request.get_json()
        saltIn = bcrypt.gensalt()
        self.loginHash = str(bcrypt.hashpw(json["password"].encode('utf8'), saltIn))
        self.id = json["id"]
        self.email = json["email"]
        self.firstName = json["firstName"]
        self.lastName = json["lastName"]
        self.salt = saltIn

    def row_to_obj(self):
        row = {
            "id" : self.id,
            "loginHash" : self.loginHash,
            "email" : self.email,
            "firstName" : self.firstName,
            "lastName" : self.lastName,
        }
        return row

    def row_to_obj_secure(self):
        row = {
            "id" : self.id,
            "email" : self.email,
            "firstName" : self.firstName,
            "lastName" : self.lastName,
        }
        return row

    def getAll():
        query = Professors.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj_secure())
        print(result, file=sys.stderr)
        return jsonify({"status": 1, "professors": result})

    def attemptLogin(request):
        json = request.get_json()
        email = json['email']
        password = json['password']
        prof = Professors.query.filter_by(email=email).first()
        print(prof, file=sys.stderr)
        if prof is None:
            print('user not found', file=sys.stderr)
            return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404
        hashedInput = str(bcrypt.hashpw(password.encode('utf8'), prof.salt))
        print(prof.loginHash, file=sys.stderr)
        print(hashedInput, file=sys.stderr)
        if(prof.loginHash == hashedInput):
            #TODO: change to returning session ID
            return jsonify({"status":1,"professor":prof.row_to_obj_secure()}), 200
        else:
            return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404

class TAs(db.Model):#taIdentifier is PotentialTAs.id, classForApp id ClassesForApp.id
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    loginHash = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    firstName = db.Column(db.String(64), nullable=False)
    lastName = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(64), nullable=False)
    major = db.Column(db.String(64), nullable=False)
    cum_gpa = db.Column(db.Float, nullable=False)
    expected_grad = db.Column(db.String, nullable=False)
    prev_TA = db.Column(db.Boolean, nullable=False)#Previously a TA?
    salt = db.Column(db.String, nullable=False)

    def __init__(self, request):
        json = request.get_json()
        saltIn = bcrypt.gensalt()
        self.id = json["id"]
        self.loginHash = str(bcrypt.hashpw(json["password"].encode('utf8'), saltIn))
        self.email = json["email"]
        self.firstName = json['firstName']
        self.lastName = json['lastName']
        self.phone = json['phone']
        self.major = json['major']
        self.cum_gpa = json['cum_gpa']
        self.expected_grad = json['expected_grad']
        self.prev_TA = json['prev_TA']
        self.salt = saltIn

    def attemptLogin(request):
        json = request.get_json()
        email = json['email']
        password = json['password']
        ta = TAs.query.filter_by(email=email).first()
        print(ta, file=sys.stderr)
        if ta is None:
            print('user not found', file=sys.stderr)
            return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404
        hashedInput = str(bcrypt.hashpw(password.encode('utf8'), ta.salt))
        print(ta.loginHash, file=sys.stderr)
        print(hashedInput, file=sys.stderr)
        if(ta.loginHash == hashedInput):
            #TODO: change to returning session ID
            return jsonify({"status":1,"professor":ta.row_to_obj_secure()}), 200
        else:
            return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404

    def row_to_obj(self):
        row = {
            'id':self.id,
            'loginHash':self.loginHash,
            'email':self.email,
            'firstName':self.firstName,
            'lastName':self.lastName,
            'phone':self.phone,
            'major':self.major,
            'cum_gpa':self.cum_gpa,
            'expected_grad':self.expected_grad,
            'prev_TA':self.prev_TA,
            'salt':self.salt
        }
        return row

    def row_to_obj_secure(self):
        row = {
        'id':self.id,
        'email':self.email,
        'firstName':self.firstName,
        'lastName':self.lastName,
        'phone':self.phone,
        'major':self.major,
        'cum_gpa':self.cum_gpa,
        'expected_grad':self.expected_grad,
        'prev_TA':self.prev_TA
        }
        return row

    def getAll():
        query = TAs.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj_secure())
        print(result, file=sys.stderr)
        return jsonify({"status": 1, "tas": result})
