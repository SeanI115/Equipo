from __main__ import app
from flask import Flask, jsonify, request, redirect, url_for
from sqlalchemy import and_
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
            "email" : self.email,
            "firstName" : self.firstName,
            "lastName" : self.lastName
        }
        return row

    def getAll():
        query = Professors.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj())
        return jsonify({"status": 1, "professors": result}), 200

    def getProfByID(id):
        validated = Sessions.validateSessionIDRole(id, 'prof')
        if(validated):
            prof = Professors.query.filter_by(id=id).first()
            return jsonify({'status':1,'prof':prof.row_to_obj()}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

    def attemptLogin(request):
        json = request.get_json()
        email = json['email'].lower()
        password = json['password']
        prof = Professors.query.filter_by(email=email).first()
        if prof is None:
            return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404
        hashedInput = str(bcrypt.hashpw(password.encode('utf8'), prof.salt))
        if(prof.loginHash == hashedInput):
            Sessions.createSession(prof.id, "prof")
            #return jsonify({"status":1,"professor":prof.row_to_obj()}), 200
            return jsonify({"status":1,"loggedIn":prof.row_to_obj()}), 200
        else:
            return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404

    def editProf(request):
        json=request.get_json()
        toEdit=Professors.query.filter_by(id=json['id']).first()
        toEdit.firstName = json['firstName']
        toEdit.lastName = json['lastName']
        db.session.add(toEdit)
        db.session.commit()
        db.session.refresh(toEdit)
        return jsonify({"status":1,"edited":toEdit.row_to_obj()}), 200

    def deleteProf(request):
        json = request.get_json()
        validated = Sessions.validateSession(request)
        requestedID = json['requestedID']
        prof = Professors.query.filter_by(id=requestedID).first()
        classes = ClassesForApp.query.filter_by(professorID=prof.id).all()
        for row in classes:
            Applications.query.filter_by(classID=row.id).delete()
            db.session.commit()
        ClassesForApp.query.filter_by(professorID=prof.id).delete()
        db.session.commit()
        Professors.query.filter_by(id=requestedID).delete()
        db.session.commit()
        return jsonify({"status":1,"deleted":requestedID}),200

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
        if ta is None:
            return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404
        hashedInput = str(bcrypt.hashpw(password.encode('utf8'), ta.salt))
        if(ta.loginHash == hashedInput):
            Sessions.createSession(ta.id, "ta")
            return jsonify({"status":1,"loggedIn":ta.row_to_obj()}), 200
        else:
            return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404

    def deleteTA(request):
        json = request.get_json()
        validated = Sessions.validateSession()
        if validated:
            requestedID = json['requestedID']
            Applications.query.filter_by(studentID=requestedID).delete()
            db.session.commit()
            TAs.query.filter_by(id=requestedID).delete()
            db.session.commit()
            return jsonify({"status:1"}),200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

    def row_to_obj(self):
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
            result.append(row.row_to_obj())
        return jsonify({"status": 1, "tas": result}), 200

    def getByID(id):
        requestedID = id
        validated = Sessions.validateSessionIDRole(id, 'ta')
        toReturn = TAs.query.filter_by(id = requestedID).first()
        if toReturn is None:
            return jsonify({"status":-1,"errors":"TA not found"}), 401
        else:
            return jsonify({"status":1,"ta":toReturn.row_to_obj()}), 200

    def editTA(request):
        json=request.get_json()
        toEdit=TAs.query.filter_by(id=json['id']).first()
        toEdit.firstName = json['firstName']
        toEdit.lastName = json['lastName']
        toEdit.major = json['major']
        toEdit.cum_gpa = json['cum_gpa']
        toEdit.expected_grad = json['expected_grad']
        toEdit.prev_TA = json['prev_TA']
        toEdit.phone = json['phone']
        db.session.add(toEdit)
        db.session.commit()
        db.session.refresh(toEdit)
        return jsonify({"status":1,"edited":toEdit.row_to_obj()}), 200

class ClassesForApp(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False)
    professorID = db.Column(db.String, nullable=False)
    prefix = db.Column(db.String(5), nullable=False)
    courseNumber = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String, nullable=False)
    numTAsNeeded = db.Column(db.Integer, nullable=False)
    numTAsAdded = db.Column(db.Integer, nullable=False, default=0)
    TAsAddedList = db.Column(db.String, nullable=False, default='')
    labSection = db.Column(db.String, nullable=True)
    dayTime = db.Column(db.String, nullable=True)

    def __init__(self, request):
        json = request.get_json()
        self.id=str(uuid.uuid4())
        self.professorID=json['professorID']
        self.prefix=json['prefix'].upper()
        self.courseNumber=json['courseNumber']
        self.semester = json['semester']
        self.numTAsNeeded=json['numTAsNeeded']
        self.numTAsAdded=json['numTAsAdded']
        self.TAsAddedList=''
        self.labSection=json['labSection']
        self.dayTime=json['dayTime']

    def row_to_obj(self):
        prof = Professors.query.filter_by(id=self.professorID).first()
        row = {
            'id':self.id,
            'professorID':self.professorID,
            'prefix':self.prefix,
            'courseNumber':self.courseNumber,
            'semester':self.semester,
            'numTAsNeeded':self.numTAsNeeded,
            'numTAsAdded':self.numTAsAdded,
            'labSection':self.labSection,
            'dayTime':self.dayTime,
            "email" : prof.email,
            "firstName" : prof.firstName,
            "lastName" : prof.lastName
        }
        return row

    def getAll():
        query = ClassesForApp.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj())
        return jsonify({"status": 1, "classes": result}), 200

    def getClassPrefixes(request):
        prefixes = set()
        for prefix in ClassesForApp.query.distinct(ClassesForApp.prefix):
            prefixes.add(prefix.prefix)
        return jsonify({"status": 1, "prefixes": list(prefixes)}), 200

    def getCourseNumbers(prefix):
        numbers = set()
        for number in ClassesForApp.query.filter_by(prefix=prefix).distinct(ClassesForApp.courseNumber):
            numbers.add(number.courseNumber)
        return jsonify({"status":1,"numbers":list(numbers)}), 200

    def getClassesByProfId(profid, role):
        validated = Sessions.validateSessionIDRole(profid,role)
        if validated:
            classes = ClassesForApp.query.filter_by(professorID = profid).all()
            result = []
            for row in classes:
                result.append(row.row_to_obj())
            return jsonify({"status": 1, "classes": result}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

    def getClassesByPrefix(prefix, id):
        validated = Sessions.validateSessionIDRole(id, 'ta')
        if validated:
            query = ClassesForApp.query.filter_by(prefix=prefix)
            classes = []
            for row in query:
                classes.append(row.row_to_obj())
            return jsonify({"status": 1, "classes": classes}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

    def addTAToClass(request):
        json = request.get_json()
        acceptedApp = Applications.query.filter_by(id=json['id']).first()
        acceptedApp.accepted = True
        db.session.add(acceptedApp)
        db.session.commit()
        db.session.refresh(acceptedApp)
        classToAddID = acceptedApp.classID
        classToAdd = ClassesForApp.query.filter_by(id=classToAddID).first()
        if classToAdd:
            student = TAs.query.filter_by(id=acceptedApp.studentID).first()
            if student:
                classToAdd.TAsAddedList += ','
                classToAdd.TAsAddedList += str(student.id)
                classToAdd.numTAsAdded+=1
                db.session.add(classToAdd)
                db.session.commit()
                db.session.refresh(classToAdd)
                return jsonify({"status":1,"class":classToAdd.row_to_obj()}), 200
            else:
                return jsonify({"status":-1,"errors":"student not found"}), 404
        else:
            return jsonify({"status":-1,"errors":"class not found"}), 404

    def deleteClassByID(request):
        json = request.get_json
        requestedID = json['requestedID']
        validated = Sessions.validateSession(request)
        if validated:
            Applications.query.filter_by(classID=requestedID).delete()
            db.session.commit()
            ClassesForApp.query.filter_by(id=requestedID)
            db.session.commit()
            return jsonify({"status":1}),200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

class Applications(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False)
    studentID = db.Column(db.String, nullable=False)
    classID = db.Column(db.String, nullable=False)
    gradeInClass = db.Column(db.String, nullable=False)
    story = db.Column(db.String, nullable=True)
    accepted = db.Column(db.Boolean, nullable=False)

    def __init__(self, request):
        json = request.get_json()
        self.id = str(uuid.uuid4())
        self.studentID = json['studentID']
        self.classID = json['classID']
        self.gradeInClass = json['gradeInClass']
        self.story = json['story']
        self.accepted = False

    def row_to_obj(self):
        classForApp = ClassesForApp.query.filter_by(id=self.classID).first()
        prof = Professors.query.filter_by(id=classForApp.professorID).first()
        ta = TAs.query.filter_by(id=self.studentID).first()
        row = {
            'id':self.id,
            'studentID':self.studentID,
            'classID':self.classID,
            'gradeInClass':self.gradeInClass,
            'story':self.story,
            'accepted':self.accepted,
            'prefix':classForApp.prefix,
            'courseNumber':classForApp.courseNumber,
            'semester':classForApp.semester,
            'numTAsNeeded':classForApp.numTAsNeeded,
            'numTAsAdded':classForApp.numTAsAdded,
            'labSection':classForApp.labSection,
            'dayTime':classForApp.dayTime,
            "profEmail" : prof.email,
            "profFirstName" : prof.firstName,
            "profLastName" : prof.lastName,
            'TAemail':ta.email,
            'TAFirstName':ta.firstName,
            'TALastName':ta.lastName,
            'TAphone':ta.phone,
            'TAmajor':ta.major,
            'TAcum_gpa':ta.cum_gpa,
            'TAexpected_grad':ta.expected_grad,
            'TAprev_TA':ta.prev_TA
        }
        return row

    def getAll():
        query = Applications.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj())
        return jsonify({"status": 1, "applications": result}), 200

    def getAppsByTAID(requestedID):
        query = Applications.query.filter_by(studentID=requestedID).all()
        apps = []
        for row in query:
            apps.append(row.row_to_obj())
        return jsonify({"status": 1, "apps": apps}), 200

    def getAppsForClass(requestedID):
        query = Applications.query.filter_by(classID=requestedID).all()
        apps = []
        for row in query:
            apps.append(row.row_to_obj())
        return jsonify({"status": 1, "apps": apps}), 200

    def deleteAppByID(request):
        validated = Sessions.validateSession()
        if validated:
            Applications.query.filter_by(id=request.args.get('requestedID')).delete()
            return jsonify({'status':1}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

class Sessions(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False)
    userID = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    expiration = db.Column(db.DateTime(timezone=False), nullable=False)

    def __init__(self, userID, role, now=None):
        self.id = str(uuid.uuid4())
        self.userID = userID
        self.role = role
        if not now:
            now = datetime.datetime.utcnow()
        self.expiration = now+datetime.timedelta(hours=SESSION_EXPIRATION_HOURS)


    def row_to_obj(self):
        row = {
            'id':self.id,
            'userId':self.userID,
            'role':self.role,
            'expiration':self.expiration
        }
        return row

    def getAll():#TESTING ONLY
        query = Sessions.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj())
        return jsonify({"status": 1, "sessions": result}), 200

    def validateSession(request):
        json = request.get_json()
        userID = json['userID']
        role = json['role']
        query = Sessions.query.filter(and_(Sessions.userID == userID, Sessions.role == role, Sessions.expiration>=datetime.datetime.utcnow())).first()
        if query is None:
            return False
        else:
            return True

    def validateSessionIDRole(id, role):
        query = Sessions.query.filter(and_(Sessions.userID == id, Sessions.role == role, Sessions.expiration>=datetime.datetime.utcnow())).first()
        if query is None:
            return False
        else:
            return True

    def createSession(userId, role):
        newSession = Sessions(userId, role)
        db.session.add(newSession)
        db.session.commit()
        db.session.refresh(newSession)
        return ''
