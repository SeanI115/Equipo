from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
import bcrypt, datetime, sys, uuid

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = sqlalchemy.SQLAlchemy(app)
base_url = '/api/'
######### START OF WORKING CODE
class Professors(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False)#is email
    loginHash = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.String, nullable=False)


    def __init__(request):
        json = request.get_json()
        saltIn = bcrypt.gensalt()
        self.hashed = str(bcrypt.hashpw(json["password"].encode('utf8'), saltIn))
        self.id = json["id"]
        self.email = json["email"]
        self.firstName = json["firstName"]
        self.lastName = json["lastName"]
        self.salt = saltIn

def row_to_obj_prof(row):
    row = {
        "id" : row.id,
        "loginHash" : row.loginHash,
        "email" : row.email,
        "firstName" : row.firstName,
        "lastName" : row.lastName,
    }
    return row

def row_to_obj_prof_secure(row):
    row = {
        "id" : row.id,
        "email" : row.email,
        "firstName" : row.firstName,
        "lastName" : row.lastName,
    }
    return row

@app.route(base_url+'create/<string:role>',methods=["POST"])
def create(role):
    newThing = ''
    if role is 'Prof':
        newThing = Professors(request)
    elif role is 'TA':
        newThing = TAs(request)
    else:
        return jsonify({"status":-1,"error":"invalid role"}), 500
    print(prof, file=sys.stderr)
    db.session.add(newThing)
    db.session.commit()
    db.session.refresh(newThing)
    if role is 'Prof':
        return jsonify({"status":1,"professor":row_to_obj_prof_secure(newThing)}), 200
    else role is 'TA':
        return jsonify({"status":1,"ta":row_to_obj_ta_secure(newThing)}), 200

@app.route(base_url+'Profs',methods=["GET"])
def getAllProfs():
    query = Professors.query.all()
    result = []
    for row in query:
        result.append(
            row_to_obj_prof_secure(row) # you must call this function to properly format
        )
    print(result, file=sys.stderr)
    return jsonify({"status": 1, "professors": result})

class TAs(db.Model):#taIdentifier is PotentialTAs.id, classForApp id ClassesForApp.id
    id = db.Column(db.String, primary_key=True, nullable=False)
    loginHash = db.Column(db.String, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    firstName = db.Column(db.String(64), nullable=False)
    lastName = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(64))
    major = db.Column(db.String(64))
    cum_gpa = db.Column(db.String)
    expected_grad = db.Column(db.String)
    prev_TA = db.Column(db.Boolean)#Previously a TA?
    salt = db.Column(db.String)

    def __init__(request):
        json = request.get_json()
        saltIn = bcrypt.gensalt()
        self.hashed = str(bcrypt.hashpw(json["id"], json["password"].encode('utf8'), salt))
        self.email = json["email"]
        self.firstName = json["firstName"]
        self.lastName = json["lastName"]
        self.phone = json["phone"]
        self.major = json["major"]
        self.cum_gpa = json["cum_gpa"]
        self.expected_grad = json["expected_grad"]
        self.prev_TA = json["prev_TA"]
        self.salt = saltIn

def row_to_obj_ta(row):
    row = {
            "id": row.id,
            "loginHash": row.loginHash,
            "email": row.email,
            "firstName": row.firstName,
            "lastName": row.lastName,
            "phone": row.phone,
            "major": row.major,
            "cum_gpa": row.cum_gpa,
            "expected_grad": row.expected_grad,
            "prev_TA": row.prev_TA,
            "salt": row.salt
        }
    return row

#same as row_to_obj_potential_ta but no salt or hash
def row_to_obj_ta_secure(row):
    row = {
            "id": row.id,
            "email": row.email,
            "firstName": row.firstName,
            "lastName": row.lastName,
            "phone": row.phone,
            "major": row.major,
            "cum_gpa": row.cum_gpa,
            "expected_grad": row.expected_grad,
            "prev_TA": row.prev_TA
        }
    return row

@app.route(base_url+'TAs',methods=["GET"])
def getAllTAs():
    query = TAs.query.all()
    result = []
    for row in query:
        result.append(row_to_obj_ta_secure(row))
    return jsonify({"status": 1, "TAs": result})
##########END OF WORKING CODE

@app.route(base_url+'loginProf',methods=['POST'])
def loginProf():
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
        return jsonify({"status":1,"professor":row_to_obj_prof_secure(prof)}), 200
    else:
        return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404

@app.route(base_url+'loginTA',methods=['POST'])
def loginTA():
    json = request.get_json()
    email = json['email']
    password = json['password']
    TA = TAs.query.filter_by(email=email).first()
    print(TA, file=sys.stderr)
    if TA is None:
        print('user not found', file=sys.stderr)
        return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404
    hashedInput = str(bcrypt.hashpw(password.encode('utf8'), TA.salt))
    print(TA.loginHash, file=sys.stderr)
    print(hashedInput, file=sys.stderr)
    if(TA.loginHash == hashedInput):
        #TODO: change to returning session ID
        return jsonify({"status":1,"TA":row_to_obj_ta_secure(TA)}), 200
    else:
        return jsonify({"status":-1,"errors":"Email or Password Incorrect"}), 404

class Sessions(db.Model):
    id=db.Column(db.String, primary_key=True, nullable=False)
    role=db.Column(db.String)
    userID=db.column(db.String)
    expiration=db.Column(db.DateTime, nullable=False)

    def __init__(self, id, role, userID, expiration):
        self.id = id
        self.role = role
        self.userID = userID
        self.expiration = expiration

def createSession(role, userID):
    sessionID = str(uuid.uuid4)
    expiration = datetime.utcnow() + datetime.timedelta(hours=2)
    newSession = Sessions(sessionID, role, userID, expiration)
    db.session.add(newSession)
    db.session.commit()
    db.session.refresh(newSession)
    return sessionID


def main():
    db.create_all() # creates the tables you've provided
    app.run()       # runs the Flask application

if __name__ == '__main__':
    main()
