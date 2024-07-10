#!/usr/bin/env python3

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy  import SQLAlchemy
from flask_restful import Api, Resource
from flask import Flask, jsonify, request, make_response

from models import db, Department,Patient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)



class Home(Resource):

    def get(self):

        response_dict = {
            "message": "Welcome to the Welcome to Health Application",
        }

        response = make_response(
            response_dict,
            200
        )

        return response

api.add_resource(Home, '/')

class Patients(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Patients.querry.all()]
        response = make_response(
            response_dict_list,
            200)
        return response
    
    def post(self):
        new_record = Patient(
            name=request.form['name'],
            age=request.form['age'],
            gender=request.form['gender'],
            phone_number=request.form['phone_number'],
            diagnosis=request.form['diagnosis'],
            email=request.form['email']
        )
        db.session.add(new_record)
        db.session.commit()
        response_dict = new_record.to_dict()
        
        response = make_response(
            response_dict,
            201)
        return response
    
api.add_resource(Patients, '/patients')

# api.add_resource(PatientByID, '/patients/<int:id>')
    
# api.add_resource(Departments, '/departments')

if __name__ == '__main__':
    app.run(port=5555, debug=True)