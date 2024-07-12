#!/usr/bin/env python3

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy  import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash,Bcrypt
from sqlalchemy import and_, not_


from models import db, Department,Patient

app = Flask(__name__)
# configure db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"


migrate = Migrate(app, db)

# setup migration tool
db.init_app(app)

api = Api(app)

# initialize bcrypt
bcrypt = Bcrypt(app)

# setup jwt
jwt = JWTManager(app)



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

class PatientResource(Resource):
     # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True,
                        help="First name is required")
    parser.add_argument('age', required=True,
                        help="Age is required")
    parser.add_argument('gender', required=True,
                        help="Gender is required")
    parser.add_argument('phone_number', required=True,
                        help="Phone number is required")
    parser.add_argument('diagnosis', required=True,
                        help="Diagnosis is required")
    parser.add_argument('email', required=True,
                        help="Email is required")
    @jwt_required()
    def get(self, id=None):
        jwt = get_jwt()
        if jwt['role'] != 'admin':
            return {"messgae":"Unauthorized request"}, 401   
        if id == None:
            patients = Patient.query.all()
            results = []
            
            for patient in patients:
                results.append(patient.to_dict())
                
            return results 
        else:
            patient = Patient.query.filter_by(id=id).first()
            if patient == None:
                return {"message": "Patient not found"}, 404
            return patient.to_dict()
        
    def post(self):
        data= PatientResource.parser.parse_args()
        
        # verify email and phone numbers are available
        email= Patient.query.filter_by(email=data['email']).first()
        if email:
            return {"message": "Email already exists"}, 422
        phone= Patient.query.filter_by(phone_number=data['phone_number']).first()
        if phone:
            return {"message": "Phone number already exists"}, 422
        
        patient= Patient(**data)
        
        db.session.add(patient)
        db.session.commit()
        
        return {"message": "Patient created successfully"}
    
    def delete (self,id):
        patient = Patient.query.filter_by(id=id).first()
        if patient == None:
            return {"message": "Patient not found"}, 404
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted successfully"}
    
            
        
api.add_resource(PatientResource,'/patients','/patients/<int:id>')
        
        
#     def get(self):
#         response_dict_list = [n.to_dict() for n in Patient.query.all()]
#         response = make_response(
#             response_dict_list,
#             200)
#         return response
    
#     def post(self):
#         new_record = Patient(
#             name=request.form['name'],
#             age=request.form['age'],
#             gender=request.form['gender'],
#             phone_number=request.form['phone_number'],
#             diagnosis=request.form['diagnosis'],
#             email=request.form['email']
#         )
#         db.session.add(new_record)
#         db.session.commit()
#         response_dict = new_record.to_dict()
        
#         response = make_response(
#             response_dict,
#             201)
#         return response
    
# api.add_resource(Patients, '/patients')

# class PatientByID(Resource):
#     def get(self, id):
#         response_dict = Patient.query.filter_by(id=id).first().to_dict()
#         response= make_response(response_dict, 200)
#         return response
    
#     def delete(self,id):
#         record = Patient.query.filter_by(id=id).first()
#         if record:
#             db.session.delete(record)
#             db.session.commit()
#             response_dict = {"message": "Patient deleted successfully"}
#             response = make_response(response_dict, 200)
#         else:
#             response_dict = {"message": "Patient not found"}
#             response = make_response(response_dict, 404)
#         return response

# api.add_resource(PatientByID, '/patients/<int:id>')

class DepartmentResource(Resource):
    def get(self):
        results = []
        
        for department in Department.query.all():
            results.append(department.to_dict())
            
        return make_response(jsonify(results), 200)
   
   
    def post(self):

        new_record = Department(
            name=request.form['name']
        )  
        db.session.add(new_record)
        db.session.commit()
        response_dict = new_record.to_dict()
        response = make_response(
            response_dict,
            201)
        return response
    
api.add_resource(DepartmentResource, '/departments_all')

if __name__ == '__main__':
    app.run(port=5000, debug=True)