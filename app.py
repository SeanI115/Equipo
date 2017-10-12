from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy

import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'

db = sqlalchemy.SQLAlchemy(app)

class PotentialTAs(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    loginHash = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    firstName = db.Column(db.String(64), nullable=False)
    lastName = db.Column(db.String(64), nullable=False)
    gpa = db.Column(db.Float, nullable=False)
    # TODO 1: add all of the columns for the other table attributes

class TAApplications(db.Model):#taIdentifier is PotentialTAs.id, classForApp id ClassesForApp.id
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    taIdentifier = db.Column(db.Integer, secondary_key=True, nullable=False)
    story = db.Column(db.String(1024), nullable=False)
    classForApp = db.Column(db.String, nullable=False)
    gradeInClass = db.Column(db.String, nullable=False)

class ClassesForApp(db.Model):
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    subject = db.Column(db.String(10), nullable=False)
    courseNumber = db.Column(db.Integer, nullable=False)
    courseDescription = db.Column(db.String(1024), nullable=False)

class Professors(db.Model):
    id = db.Column(db.Integer, primary_key=true, nullable=False)
    loginHash = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)

base_url = '/api/'

# index
# loads all smiles given a space, count parameter and order_by parameter 
# if the count param is specified and doesn't equal all limit by the count
# if the order_by param is specified order by param otherwise load by updated_at desc
# return JSON
@app.route(base_url + 'smiles',methods=["GET"])
def index():
    space = request.args.get('space', None) 

    if space is None:
        return "Must provide space", 500

    count = request.args.get('count', None)
    order_by = request.args.get('order_by', None)
    
    query = Smile.query.all()
    
    # TODO 2: set the column which you are ordering on (if it exists)
    if order_by is not None:
        Smile.query.order_by(order_by)
    # TODO 3: limit the number of posts based on the count (if it exists)
    if count is not None:
        Smile.query.limit(count)
    
    result = []
    for row in query:
        result.append(
            row_to_obj(row) # you must call this function to properly format 
        )

    return jsonify({"status": 1, "smiles": result})


# show
# loads a smile given the id as a value in the URL
# TODO 4: create the route for show
@app.route(base_url+'smiles/<int:id>',methods=["GET"])
def show(id):
    row=Smile.query.filter_by(id=id).first()
    return jsonify({"smile": row_to_obj(row),"status":1}), 200

# create
# creates a smile given the params
# TODO 5: create the route for create
@app.route(base_url+'smiles',methods=["POST"])
def create():
    smile = Smile(**request.json)
    db.session.add(smile)
    db.session.commit()
    db.session.refresh(smile)
    return jsonify({"status":1,"smiles":row_to_obj(smile)}), 200

# delete_smiles
# delete given an space
# delete all smiles in that space
# TODO 6: create the route for delete_smiles
@app.route(base_url+'smiles',methods=["DELETE"])
def delete():
    space = request.args.get('space', None) 

    if space is not None:
        Smile.query.filter_by(space=space).delete()
        db.session.commit()
        return jsonify({"status:1"}),200
    else:
        return jsonify({"status":-1,"errors":"Must provide space for deletion"}), 500        

# post_like
# loads a smile given an ID and increments the count by 1
# TODO 7: create the route for post_like 
@app.route(base_url+'smiles/<int:id>/like', methods=["POST"])
def post_like(id):
    smile=Smile.query.filter_by(id=id).first()
    smile.like_count += 1;
    db.session.add(smile)
    db.session.commit()
    db.session.refresh(smile)
    return jsonify({"status":1,"smile":row_to_obj(smile)}), 200

def row_to_obj(row):
    row = {
            "id": row.id,
            "space": row.space,
            "title": row.title,
            "story": row.story,
            "happiness_level": row.happiness_level,
            "like_count": row.like_count,
            "created_at": row.created_at,
            "updated_at": row.updated_at
        }

    return row

  
def main():
    db.create_all() # creates the tables you've provided
    app.run()       # runs the Flask application  

if __name__ == '__main__':
    main()
