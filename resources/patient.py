from flask_restful import Resource, reqparse
from sqlalchemy import and_, not_
from flask_jwt_extended import jwt_required, get_jwt
from models import db, Patient


class PatientResource(Resource):
     # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True,
                        help="Name is required")
    parser.add_argument('age', required=True,
                        help="Age is required")
    parser.add_argument('gender', required=True,
                        help="Gender is required")
    parser.add_argument('phone_number', required=True,
                        help="Phone number is required")
    parser.add_argument('diagnosis', required=True,
                        help="Diagnosis is required")
    parser.add_argument('email', required=True,
                        help="Email Address is required")
    parser.add_argument('password', required=True, 
                        help="Password is required")
    @jwt_required()
    def get(self, id=None):
        
        jwt = get_jwt()
        if jwt['role'] != 'admin' or  jwt['role'] != 'doctor':
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
        print (data)
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
            return {"message": "Patient not found","status": "fail"}, 404
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted successfully"}
    
    
    
    
            
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