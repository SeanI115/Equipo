from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
import bcrypt, datetime, sys, uuid

app = Flask(__name__)
CORS(app)


from dataAccess import db, Professors, TAs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataAccessTest.db'
base_url = '/api/'
######### START OF WORKING CODE

def create(classForCreate, request):
    newThing = classForCreate(request)
    print(newThing, file=sys.stderr)
    db.session.add(newThing)
    db.session.commit()
    db.session.refresh(newThing)
    return jsonify({"status":1,'created':newThing.row_to_obj_secure()}), 200

@app.route(base_url+'createProf',methods=["POST"])
def createProf():
    return create(Professors, request)


@app.route(base_url+'Profs',methods=["GET"])
def getAllProfs():
    return Professors.getAll()

@app.route(base_url+'loginProf',methods=['POST'])
def loginProf():
    Professors.attemptLogin(request)

@app.route(base_url+'createTA',methods=["POST"])
def createTA():
    return create(TAs, request)

@app.route(base_url+'TAs',methods=["GET"])
def getAllTAs():
    return TAs.getAll()

@app.route(base_url+'loginTA',methods=['POST'])
def loginTA():
    return TAs.attemptLogin(request)

def main():
    db.create_all() # creates the tables you've provided
    app.run()       # runs the Flask application

if __name__ == '__main__':
    main()
