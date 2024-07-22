from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash
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
        if jwt['role'] == 'admin' or jwt['role'] == 'doctor':

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
        else:
            return {"messgae":"Unauthorized request"}, 401 
        
    @jwt_required()    
    def post(self):
        jwt = get_jwt()
        if jwt ['role'] == 'patient':
                    
            data= PatientResource.parser.parse_args()
            
            data['password'] = generate_password_hash(
                data['password']).decode('utf-8')
            
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
        else:
            return {"message":"Unauthorized request"}, 401
    
    
    @jwt_required()
    def delete (self,id):
        
        jwt = get_jwt()
        if jwt['role']== 'admin' or  jwt['role']== 'doctor':
            
            
            patient = Patient.query.filter_by(id=id).first()
            if patient == None:
                return {"message": "Patient not found","status": "fail"}, 404
            db.session.delete(patient)
            db.session.commit()
            return {"message": "Patient deleted successfully"}
        else:
            return {"message":"Unauthorized request"}, 401
    
    
    
