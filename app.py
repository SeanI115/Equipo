from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
import bcrypt, datetime, sys, uuid

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'

from dataAccess import db, Professors, TAs

db = sqlalchemy.SQLAlchemy(app)
base_url = '/api/'
######### START OF WORKING CODE



def create(classForCreate, request):
    newThing = classForCreate(request)
    print(newThing, file=sys.stderr)
    db.session.add(newThing)
    db.session.commit()
    db.session.refresh(newThing)
    return jsonify({"status":1,"newThing":classForCreate.row_to_obj_secure(newThing)}), 200

@app.route(base_url+'createProf',methods=[""])


@app.route(base_url+'Profs',methods=["GET"])
def getAllProfs():
    return Professors.getAll()

@app.route(base_url+'TAs',methods=["GET"])
def getAllTAs():
    query = TAs.query.all()
    result = []
    for row in query:
        result.append(row_to_obj_ta_secure(row))
    return jsonify({"status": 1, "TAs": result})

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
        self.id = str(uuid.uuid4)
        self.role = role
        self.userID = userID
        self.expiration = datetime.utcnow() + datetime.timedelta(hours=2)

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
