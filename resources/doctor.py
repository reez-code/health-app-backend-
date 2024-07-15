from flask_restful import Resource
from models import db, Doctor
from flask import  jsonify, request
import logging


class DoctorResource(Resource):
    def get(self):
        try:
            doctors = Doctor.query.all()
            doctors_dict = [doctor.to_dict() for doctor in doctors]
            logging.debug(f"Doctors fetched successfully: {doctors_dict}")
            return jsonify(doctors_dict)
        except Exception as e:
            logging.error(f"Error fetching doctors: {e}")
            return jsonify({"error": str(e)}), 500

    def post(self):
        data = request.get_json()
        required_fields = ['name', 'email', 'phone', 'specialization', 'image']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

        try:
            doctor = Doctor(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                specialization=data['specialization'],
                image=data['image']
            )
            db.session.add(doctor)
            db.session.commit()
            return jsonify(doctor.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500       

class DoctorDetailResource(Resource):
 def get(self, id):
    try:
        doctor = Doctor.query.get(id)
        if doctor is None:
            return jsonify({"error": "Doctor not found."}), 404
        return jsonify(doctor.to_dict())
    except Exception as e:
        logging.error(f"Error fetching doctor: {e}")
        return jsonify({"error": str(e)}), 500
def delete(self, id):
        doctor = Doctor.query.get(id)
        if doctor is None:
            return jsonify({"error": "Doctor not found."}), 404

        db.session.delete(doctor)
        db.session.commit()
        return jsonify({"message": "Doctor deleted successfully."}), 200