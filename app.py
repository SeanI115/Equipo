from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
import bcrypt, datetime, sys, uuid

app = Flask(__name__)
CORS(app)


from dataAccess import db, Professors, TAs, ClassesForApp, Applications, Sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
base_url = '/api/'
######### START OF WORKING CODE

def create(classForCreate, request):
    newThing = classForCreate(request)
    print(newThing, file=sys.stderr)
    db.session.add(newThing)
    db.session.commit()
    db.session.refresh(newThing)
    if(classForCreate == Professors): Sessions.createSession(newThing.id, 'prof')
    if(classForCreate == TAs): Sessions.createSession(newThing.id, 'ta')
    return jsonify({"status":1,'created':newThing.row_to_obj()}), 200

@app.route(base_url+'createProf',methods=["POST"])
def createProf():
    return create(Professors, request)


@app.route(base_url+'Profs',methods=["GET"])
def getAllProfs():
    return Professors.getAll()

@app.route(base_url+'ProfByID',methods=["GET"])
def ProfByID():
    return Professors.getProfByID(request)

@app.route(base_url+'loginProf',methods=['POST'])
def loginProf():
    return Professors.attemptLogin(request)

@app.route(base_url+'deleteProf',methods=["DELETE"])
def deleteProf():
    return Professors.deleteProf(request)

@app.route(base_url+'createTA',methods=["POST"])
def createTA():
    return create(TAs, request)

@app.route(base_url+'TAs',methods=["GET"])
def getAllTAs():
    return TAs.getAll()

@app.route(base_url+'loginTA',methods=['POST'])
def loginTA():
    return TAs.attemptLogin(request)

@app.route(base_url+'TAByID',methods=["GET"])
def getTAByID():
    return TAs.getByID(request)

@app.route(base_url+'createClass',methods=["POST"])
def createClass():
    return create(ClassesForApp, request)

@app.route(base_url+'Classes',methods=["GET"])
def getAllClasses():
    return ClassesForApp.getAll()

@app.route(base_url+'ClassesByProfID/<string:profid>/<string:role>/',methods=["GET"])
def getClassesByProfID(profid, role):
    print(profid)
    print(role)
    return ClassesForApp.getClassesByProfId(profid, role)

@app.route(base_url+'ClassPrefixes',methods=["GET"])
def getClassPrefixes():
    return ClassesForApp.getClassPrefixes(request)

@app.route(base_url+'ClassesByPrefix',methods=["GET"])
def getClassesByPrefix():
    return ClassesForApp.getClassesByPrefix(request)

@app.route(base_url+'DeleteClassByID',methods=["DELETE"])
def deleteClassByID():
    ClassesForApp.deleteClassByID(request)

@app.route(base_url+'createApplication',methods=["POST"])
def createApplication():
    return create(Applications, request)

@app.route(base_url+'Applications',methods=["GET"])
def getAllApplications():
    return Applications.getAll()

@app.route(base_url+'AppsByTAID',methods=["GET"])
def getAppsByTAID():
    return Applications.getAppsByTAID(request)

@app.route(base_url+'AppsForClass',methods=["GET"])
def getAppsByClass():
    return Applications.getAppsForClass(request)

@app.route(base_url+'DeleteApp',methods=["DELETE"])
def deleteAppByID():
    return Applications.deleteAppByID(request)

@app.route(base_url+'Sessions',methods=["GET"])
def getAllSessions():
    return Sessions.getAll()

def main():
    #db.create_all() # creates the tables you've provided
    app.run()       # runs the Flask application

if __name__ == '__main__':
    main()
