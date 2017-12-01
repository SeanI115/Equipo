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
            "lastName" : self.lastName
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

    def getAll():
        json = request.get_json()
        query = Professors.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj_secure())
        print(result, file=sys.stderr)
        return jsonify({"status": 1, "professors": result}), 200

    def getProfByID(request):
        validated = Sessions.validateSession()
        if(validated):
            prof = Professors.query.filter_by(id=request.args.get('requestedID'))
            return jsonify({'status':1,'professor':prof.row_to_obj_secure()}), 200
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
        validated = Sessions.validateSession()
        requestedID = json['requestedID']
        prof = Professors.query.filter_by(id=requestedID).first()
        classes = Classes.query.filter_by(professorID=prof.id).all()
        for row in classes:
            Applications.query.filter_by(classID=row.id).delete()
            db.session.commit()
        Classes.query.filter_by(professorID=prof.id).delete()
        db.session.commit()
        Professors.query.filter_by(id=requestedID).delete()
        db.session.commit()
        return jsonify({"status:1"}),200

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
        validated = Sessions.validateSession()
        if validated:
            query = TAs.query.all()
            result = []
            for row in query:
                result.append(row.row_to_obj_secure())
            print(result, file=sys.stderr)
            return jsonify({"status": 1, "tas": result}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401
        
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
    numTAsAdded = db.Column(db.Integer, nullable=False, default=0)
    TAsAddedList = db.Column(db.String, nullable=False, default='0')
    labSection = db.Column(db.String, nullable=True)
    dayTime = db.Column(db.String, nullable=True)

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
        self.labSection=request.args.get('labSection', None)
        self.dayTime=request.args.get('dayTime', None)

    def row_to_obj(self):
        prof = Professors.query.filter_by(id=self.professorID).first()
        row = {
            'id':self.id,
            'professorID':self.professorID,
            'prefix':self.prefix,
            'courseNumber':self.courseNumber,
            'semester':self.semester,
            'year':self.year,
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
        print(result, file=sys.stderr)
        return jsonify({"status": 1, "classes": result}), 200

    def getClassPrefixes(request):
        prefixes = []
        for prefix in ClassesForApp.query.distinct(ClassesForApp.prefix):
            prefixes.append(prefix)
        return jsonify({"status": 1, "prefixes": prefixes}), 200

    def getClassesByProfId(request):
        id=request.args.get('userId', None)
        validated = Sessions.validateSession(request)
        if validated:
            classes = ClassesForApp.query.filter_by(id = professorID).all()
            result = []
            for row in query:
                result.append(row.row_to_obj_with_prof())
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
                for row in query:
                    classes.append(row.row_to_obj_with_prof())
                print(classes, file=sys.stderr)
                return jsonify({"status": 1, "classes": classes}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

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

    def __init__(self, request):
        json = request.get_json()
        self.id = json['id']
        self.studentID = json['studentID']
        self.classID = json['classID']
        self.gradeInClass = json['gradeInClass']
        self.story = request.args.get('story', None)

    def row_to_obj(self):
        classForApp = ClassesForApp.query.filter_by(id=self.classID).first()
        prof = Professors.query.filter_by(id=classForApp.professorID).first()
        ta = TAs.query.filter_by(id=self.studentID)
        row = {
            'id':self.id,
            'studentID':self.studentID,
            'classID':self.classID,
            'gradeInClass':self.gradeInClass,
            'story':self.story,
            'prefix':classForApp.prefix,
            'courseNumber':classForApp.courseNumber,
            'semester':classForApp.semester,
            'year':classForApp.year,
            'numTAsNeeded':classForApp.numTAsNeeded,
            'numTAsAdded':classForApp.numTAsAdded,
            'labSection':classForApp.labSection,
            'dayTime':classForApp.dayTime,
            "profEmail" : prof.email,
            "profFirstName" : prof.firstName,
            "profLastName" : prof.lastName,
            'email':ta.email,
            'TAFirstName':ta.firstName,
            'TALastName':ta.lastName,
            'phone':ta.phone,
            'major':ta.major,
            'cum_gpa':ta.cum_gpa,
            'expected_grad':ta.expected_grad,
            'prev_TA':ta.prev_TA
        }

    def getAll():
        query = Applications.query.all()
        result = []
        for row in query:
            result.append(row.row_to_obj())
        print(result, file=sys.stderr)
        return jsonify({"status": 1, "applications": result}), 200

    def getAppsByTAID(request):
        requestedId=request.args.get('requestedId', None)
        validated= Sessions.validateSession(request)
        if validated:
            query = Applications.query.filter_by(studentID=requestedId).all()
            apps = []
            classes = []
            ta = TAs.query.filter_by(id=requestedID).first()
            for row in query:
                classes.append(row.row_to_obj())
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
            for row in query:
                classes.append(row.row_to_obj())
            return jsonify({"status": 1, "apps": apps, "classes": classes, "ta": ta}), 200
        else:
            return jsonify({"status":-1,"errors":"Session validation failed: You may need to re-login"}), 401

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
        return jsonify({"status": 1, "sessions": result}), 200

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
