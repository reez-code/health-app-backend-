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
        
        if jwt['role']!= 'admin' or  jwt['role']!= 'doctor':
            return {"messgae":"Unauthorized request"}, 401
        
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
        
    @jwt_required()
    def patch(self,id):
        jwt = get_jwt()
        if jwt['role']!= 'admin':
                return {"message":"Unauthorized request"}, 401
            
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
        
    @jwt_required()
    def delete(self, id):
        jwt = get_jwt()
        if jwt['role'] != 'admin':
            return {"message":"Unauthorized request"}, 401
        
        doctor = Doctor.query.filter_by(id=id).first()
        if doctor == None:
            return {"message": "Doctor not found", "status": "fail"}, 404
        
        db.session.delete(doctor)
        db.session.commit()
        return {"message": "Doctor deleted successfully"}
        
          

        

















# class DoctorResource(Resource):
#     def get(self):
#         try:
#             doctors = Doctor.query.all()
#             doctors_dict = [doctor.to_dict() for doctor in doctors]
#             logging.debug(f"Doctors fetched successfully: {doctors_dict}")
#             return jsonify(doctors_dict)
#         except Exception as e:
#             logging.error(f"Error fetching doctors: {e}")
#             return jsonify({"error": str(e)}), 500

#     def post(self):
#         data = request.get_json()
#         required_fields = ['name', 'email', 'phone', 'specialization', 'image']
#         missing_fields = [field for field in required_fields if field not in data]
#         if missing_fields:
#             return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

#         try:
#             doctor = Doctor(
#                 name=data['name'],
#                 email=data['email'],
#                 phone=data['phone'],
#                 specialization=data['specialization'],
#                 image=data['image']
#             )
#             db.session.add(doctor)
#             db.session.commit()
#             return jsonify(doctor.to_dict()), 201
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"error": str(e)}), 500       

# class DoctorDetailResource(Resource):
#  def get(self, id):
#     try:
#         doctor = Doctor.query.get(id)
#         if doctor is None:
#             return jsonify({"error": "Doctor not found."}), 404
#         return jsonify(doctor.to_dict())
#     except Exception as e:
#         logging.error(f"Error fetching doctor: {e}")
#         return jsonify({"error": str(e)}), 500
# def delete(self, id):
#         doctor = Doctor.query.get(id)
#         if doctor is None:
#             return jsonify({"error": "Doctor not found."}), 404

#         db.session.delete(doctor)
#         db.session.commit()
#         return jsonify({"message": "Doctor deleted successfully."}), 200