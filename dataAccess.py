from __main__ import app
from flask import Flask, jsonify, request
import flask_sqlalchemy as sqlalchemy
import bcrypt, datetime, sys, uuid
db = sqlalchemy.SQLAlchemy(app)
SESSION_EXPIRATION_HOURS = 1

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
        self.email = json["email"].lower()
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
            "lastName" : self.lastName
        }
        return row

    def getAll(request):
        json = request.get_json()
        validated = validateSession(json['userId'], json['role'])
        if(validated):
            query = Professors.query.all()
            result = []
            for row in query:
                result.append(row.row_to_obj_secure())
            print(result, file=sys.stderr)
            return jsonify({"status": 1, "professors": result}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

    def attemptLogin(request):
        json = request.get_json()
        email = json['email'].lower()
        password = json['password']
        prof = Professors.query.filter_by(email=email).first()
        print(prof, file=sys.stderr)
        if prof is None:
            print('user not found', file=sys.stderr)
            return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404
        hashedInput = str(bcrypt.hashpw(password.encode('utf8'), prof.salt))
        if(prof.loginHash == hashedInput):
            Sessions.createSession(prof.id, "professor")
            return jsonify({"status":1,"professor":prof.row_to_obj_secure()}), 200
        else:
            return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404

    def deleteProf(request):
        json = request.get_json()
        validated = validateSession()

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
        self.email = json["email"].lower()
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
        email = json['email'].lower()
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
            Sessions.createSession(ta.id, "ta")
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

    def getByID(request):
        role = request.args.get('role', None)
        userId = request.args.get('userId', None)
        requestedId = request.args.get('requestedID', None)
        validated = False
        if(role == None):
            return jsonify({"status":-1,"errors":"role can not be None"}), 400
        elif(role=="professor"):
            validated = Sessions.validateSession(request)
        elif(role=="ta"):
            if requestedID == userID:
                validated = Sessions.validateSession(request)
            else:
                return jsonify({"status":-1,"errors":"Access Denied"}), 401
        else:
            return jsonify({"status":-1,"errors":"Access Denied"}), 401
        toReturn = TAs.query.filter_by(id = requestedID).first()
        if toReturn is None:
            return jsonify({"status":-1,"errors":"TA not found"}), 401
        else:
            return jsonify({"status":1,"ta":toReturn.row_to_obj_secure()}), 200

class ClassesForApp(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False)
    professorID = db.Column(db.String, nullable=False)
    prefix = db.Column(db.String(5), nullable=False)
    courseNumber = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    numTAsNeeded = db.Column(db.Integer, nullable=False)
    numTAsAdded = db.Column(db.Integer, nullable=False)
    TAsAddedList = db.Column(db.String, nullable=True)

    def __init__(self, request):
        json = request.get_json()
        self.id=str(uuid.uuid4())
        self.professorID=json['professorID']
        self.prefix=json['prefix']
        self.courseNumber=json['courseNumber']
        self.semester = json['semester']
        self.year = json['year']
        self.numTAsNeeded=json['numTAsNeeded']
        self.numTAsAdded=json['numTAsAdded']

    def row_to_obj(self):
        row = {
            'id':self.id,
            'professorID':self.professorID,
            'prefix':self.prefix,
            'courseNumber':self.courseNumber,
            'semester':self.semester,
            'year':self.year,
            'numTAsNeeded':self.numTAsNeeded,
            'numTAsAdded':self.numTAsAdded
        }
        return row

    def row_to_obj_with_prof(self):
        prof = Professors.query.filter_by(id=professorID).first()
        row = {
            'id':self.id,
            'prefix':self.prefix,
            'courseNumber':self.courseNumber,
            'semester':self.semester,
            'year':self.year,
            'numTAsNeeded':self.numTAsNeeded,
            'numTAsAdded':self.numTAsAdded,
            "id" : prof.id,
            "email" : prof.email,
            "firstName" : prof.firstName,
            "lastName" : prof.lastName
        }

    def getAll(request):
        query = ClassesForApp.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj())
        print(result, file=sys.stderr)
        return jsonify({"status": 1, "classes": result}), 200

    def viewClassesByProfId(request):
        id=request.args.get('userId', None)
        validated = Sessions.validateSession(request)
        if validated:
            classes = ClassesForApp.query.filter_by(id = professorID).all()
            result = []
            for row in query:
                result.append(row.row_to_obj())
            print(result, file=sys.stderr)
            return jsonify({"status": 1, "classes": result}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

    def getClassesByPrefix(request):
        validated = Sessions.validateSession(request)
        if validated:
            prefix = request.args.get('prefix', None)
            if prefix is None:
                return jsonify({"status":-1,"errors":"must include prefix"}), 500
            else:
                query = ClassesForApp.query.filter_by(prefix=prefix)
                classes = []

        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

class Applications(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False)
    studentID = db.Column(db.String, nullable=False)
    classID = db.Column(db.String, nullable=False)
    gradeInClass = db.Column(db.String, nullable=False)
    story = db.Column(db.String, nullable=True)

    def __init__(self, request):
        json = request.get_json()
        self.id = json['id']
        self.studentID = json['studentID']
        self.classID = json['classID']
        self.gradeInClass = json['gradeInClass']
        self.story = json['story']

    def row_to_obj(self):
        row = {
            'id':self.id,
            'studentID':self.studentID,
            'classID':self.classID,
            'gradeInClass':self.gradeInClass,
            'story':self.story
        }
        return row

    def getAll():
        query = Applications.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj())
        print(result, file=sys.stderr)
        return jsonify({"status": 1, "applications": result})

    def getAppsByTAID(request):
        requestedId=request.args.get('requestedId', None)
        validated= Sessions.validateSession(request)
        if validated:
            query = Applications.query.filter_by(studentID=requestedId).all()
            apps = []
            classes = []
            ta = TAs.query.filter_by(id=requestedID).first()
            for row in query:
                classForApp=ClassesForApp.query.filter_by(id=classID).first()
                apps.append(row.row_to_obj())
                classes.append(classForApp.row_to_obj())
            return jsonify({"status": 1, "apps": apps, "classes": classes, "ta": ta}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

    def getAppsForClass(request):
        requestedId=request.args.get('requestedId', None)
        validated= Sessions.validateSession(request)
        if validated:
            query = Applications.query.filter_by(classID=requestedId).all()
            apps = []
            tas = []
            classRequested = ClassesForApp.query.filter_by(id=requestedID).first()
            for row in query:
                classForApp=ClassesForApp.query.filter_by(id=classID).first()
                apps.append(row.row_to_obj())
                classes.append(classForApp.row_to_obj())
            return jsonify({"status": 1, "apps": apps, "classes": classes, "ta": ta}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

class Sessions(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False)
    userID = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    expiration = db.Column(db.DateTime(timezone=False), nullable=False)

    def __init__(self, userID, role):
        self.id = str(uuid.uuid4())
        self.userID = userID
        self.role = role
        self.expiration = datetime.datetime.utcnow+datetime.timedelta(hours=SESSION_EXPIRATION_HOURS)

    def getAll():#TESTING ONLY
        query = Sessions.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj())
        print(result, file=sys.stderr)
        return jsonify({"status": 1, "sessions": result})


    def validateSession(request):
        json = request.get_json()
        userID = json['userId']
        role = json['role']
        query = Sessions.query.filter(and_(db.Sessions.userID == userId, db.Sessions.role == role, db.Sessions.expiration>=datetime.datetime.utcnow)).first()
        if query is None:
            return False
        else:
            return True

    def createSession(userId, role):
        newSession = Sessions(userId, role)
        db.session.add(newSession)
        db.session.commit()
        db.session.refresh(newSession)
