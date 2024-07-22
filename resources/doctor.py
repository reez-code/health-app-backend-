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
          

        








