from flask_restful import Resource, reqparse
from models import db, Doctor
from flask_bcrypt import generate_password_hash
from sqlalchemy import and_, not_
from flask_jwt_extended import jwt_required, get_jwt


class DoctorResource(Resource):
     # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True,
                        help="Name is required")
    parser.add_argument('email', required=True,
                        help="Email Address is required")
    parser.add_argument('phone_number', required=True,
                        help="Phone number is required")
    parser.add_argument('specialization', required=True,
                        help="Specialization is required")
    parser.add_argument('image', required=True,
                        help="Image is required")
    parser.add_argument('password', required=True,
                        help="Password is required")
    
    @jwt_required()
    def get(self, id=None):
        
        jwt = get_jwt()
        
        if jwt['role']== 'admin' or  jwt['role']== 'doctor':
            
        
            if id == None:
                doctors = Doctor.query.all()
                results = []
                
                for doctor in doctors:
                    results.append(doctor.to_dict())
                    
                return results
            else:
                doctor = Doctor.query.filter_by(id=id).first()
                if doctor == None:
                    return {"message": "Doctor not found"}, 404
                
                return doctor.to_dict()
        else:
            return {"messgae":"Unauthorized request"}, 401
        
    @jwt_required()
    def patch(self,id):
        jwt = get_jwt()
        if jwt['role']== 'admin':
                
            data = self.parser.parse_args()
            
            data['password'] = generate_password_hash(
                data['password']).decode('utf-8')
            
            doctor = Doctor.query.filter_by(id=id).first()
            
            if doctor == None:
                return {"message": "Doctor not found"}, 404
            
            email = db.session.query(Doctor).first(
                and_(Doctor.email == data['email'], not_(Doctor.id==id))).first()
            if email:
                return {"message": "Email already exists"}, 422
            
            phone = db.session.query(Doctor).first(
                and_(Doctor.phone_number == data['phone_number'], not_(Doctor.id==id))).first()
            
            if phone:
                return {"message": "Phone number already exists"}, 422
            
            for key in data.keys():
                setattr(doctor, key, data[key])
                
                db.session.commit()
                return {"message": "Doctor updated successfully"}    
        else:
            return {"message":"Unauthorized request"}, 401
        
    @jwt_required()
    def delete(self, id):
        jwt = get_jwt()
        if jwt['role'] == 'admin':
                    
            doctor = Doctor.query.filter_by(id=id).first()
            if doctor == None:
                return {"message": "Doctor not found", "status": "fail"}, 404
            
            db.session.delete(doctor)
            db.session.commit()

            return {"message": "Doctor deleted successfully"}
        else:
            return {"message":"Unauthorized request"}, 401
    
    @jwt_required()
    def post(self):
        # Check if the user making the request is an admin
        jwt = get_jwt()
        if jwt['role'] != 'admin':
            return {"message": "Unauthorized request"}, 401

        # Parse the request data
        data = self.parser.parse_args()

        # Check if a doctor with the same email or phone number already exists
        email_exists = Doctor.query.filter_by(email=data['email']).first()
        if email_exists:
            return {"message": "Email already exists"}, 422

        phone_exists = Doctor.query.filter_by(phone_number=data['phone_number']).first()
        if phone_exists:
            return {"message": "Phone number already exists"}, 422

        # Hash the password
        hashed_password = generate_password_hash(data['password']).decode('utf-8')

        # Create a new Doctor instance
        new_doctor = Doctor(
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number'],
            specialization=data['specialization'],
            image=data['image'],
            password=hashed_password
        )

        # Add the new doctor to the database
        try:
            db.session.add(new_doctor)
            db.session.commit()
            return {"message": "Doctor created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
          

        
