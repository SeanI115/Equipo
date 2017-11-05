from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'

db = sqlalchemy.SQLAlchemy(app)

def row_to_obj_ta(row):
    row = {
            "id": row.id,
            "firstName": row.firstName,
            "lastName": row.lastName,
            "phone": row.phone,
            "major": row.major,
            "gpa": row.gpa,
            "gradDate": row.gradDate
        }
    return row

class TAs(db.Model):
    id = db.Column(db.String(64), primary_key=True, nullable=False)#this is the email
    firstName = db.Column(db.String(64), nullable=False)
    lastName = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(64))
    major = db.Column(db.String(64))
    gpa = db.Column(db.Float)
    gradDate = db.Column(db.String(64))


    def __init__(self, id, firstName, lastName, phone, major, gpa, gradDate):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.major = major
        self.gpa = gpa
        self.gradDate = gradDate


base_url = '/api/'


@app.route(base_url+'login',methods=["POST"])
def createTA():
    json = request.get_json()
    ta = TAs(**request.json)
    db.session.add(ta)
    db.session.commit()
    db.session.refresh(ta)
    return jsonify({"status":1,"TA":row_to_obj_ta(ta)}), 200

base_url = '/api/'


def main():
    db.create_all() # creates the tables you've provided
    app.run()       # runs the Flask application

if __name__ == '__main__':
    main()
