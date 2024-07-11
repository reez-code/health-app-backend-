from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime
from models import db, Doctor, Appointment, Admin, Signup
from werkzeug.security import generate_password_hash
import logging


logging.basicConfig(level=logging.DEBUG)
# Doctor Resource
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

# Appointment Resource
class AppointmentResource(Resource):
    def get(self):
        appointments = Appointment.query.all()
        appointments_dict = [appointment.to_dict() for appointment in appointments]
        return jsonify(appointments_dict)

    def post(self):
        data = request.get_json()
        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except ValueError:
            return jsonify({"error": "Invalid timestamp format. Use 'YYYY-MM-DDTHH:MM:SS' format."}), 400

        appointment = Appointment(reason=data['reason'], timestamp=timestamp)
        db.session.add(appointment)
        db.session.commit()
        return jsonify(appointment.to_dict()), 201

class AppointmentDetailResource(Resource):
    def patch(self, id):
        data = request.get_json()
        appointment = Appointment.query.get(id)
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        if 'reason' in data:
            appointment.reason = data['reason']
        if 'timestamp' in data:
            try:
                timestamp = datetime.fromisoformat(data['timestamp'])
            except ValueError:
                return jsonify({"error": "Invalid timestamp format. Use 'YYYY-MM-DDTHH:MM:SS' format."}), 400
            appointment.timestamp = timestamp

        db.session.commit()
        return jsonify(appointment.to_dict()), 200

    def delete(self, id):
        appointment = Appointment.query.get(id)
        if appointment is None:
            return jsonify({"error": "Appointment not found."}), 404

        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"message": "Appointment deleted successfully."}), 200

# Admin Resource
class AdminResource(Resource):
    def get(self):
        admins = Admin.query.all()
        admins_dict = [admin.to_dict() for admin in admins]
        return jsonify(admins_dict)

# Signup Resource
class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        required_fields = ['email', 'password','name']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

        try:
            hashed_password = generate_password_hash(data['password'])
            new_user = Signup(
                name=data['name'],
                email=data['email'],
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
