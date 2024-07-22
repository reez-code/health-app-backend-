from flask_restful import Resource, reqparse
from models import db, Specialization
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy import and_, not_
from models import db,  Admin, Doctor, Appointment, Patient, Specialization
from flask_bcrypt import generate_password_hash
import logging


class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        required_fields = ['email', 'password', 'username', 'role']
        missing_fields = [
            field for field in required_fields if field not in data]
        if missing_fields:
            return {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 400

        role = data['role'].lower()
        email_exists = Patient.query.filter_by(email=data['email']).first() or \
            Doctor.query.filter_by(email=data['email']).first() or \
            Admin.query.filter_by(email=data['email']).first()

        if email_exists:
            return {"error": "Email already exists."}, 400

        try:
            hashed_password = generate_password_hash(data['password'])

            if role == 'patient':
                new_user = Patient(
                    name=data['username'],
                    email=data['email'],
                    password=hashed_password
                )
            elif role == 'doctor':
                new_user = Doctor(
                    name=data['username'],
                    email=data['email'],
                    password=hashed_password
                )
            elif role == 'admin':
                new_user = Admin(
                    name=data['username'],
                    email=data['email'],
                    password=hashed_password
                )
            else:
                return {"error": "Invalid role specified"}, 400

            db.session.add(new_user)
            db.session.commit()
            return {"message": f"User registered successfully as {role}."}, 201

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 50


# Admin Resource
class AdminResource(Resource):
    # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help="Name is required")
    parser.add_argument('email', required=True, help="Email is required")
    parser.add_argument('phone_number', required=True,
                        help="Phone number is required")
    parser.add_argument('password', required=True, help="Password is required")

    @jwt_required()
    def get(self, id=None):
        jwt = get_jwt()
        if jwt['role'] != 'admin':
            return {"messgae": "Unauthorized request"}, 401

        if id == None:
            admins = Admin.query.all()
            results = []

            for admin in admins:
                results.append(admin.to_dict())

                return results
        else:
            admin = Admin.query.filter_by(id=id).first()

            if admin == None:
                return {"message": "Admin not found"}, 404
            return admin.to_dict()


class AppointmentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('reason', required=True, help="Reason is required")
    parser.add_argument('date_time', required=True, help="Timestamp is required in ISO 8601 format")

    @jwt_required()
    def get(self, id=None):
        jwt = get_jwt()
        user_id = get_jwt_identity()

        if jwt['role'] == 'patient':
            if id is None:
                # Patients can only see their own appointments
                appointments = Appointment.query.filter_by(patient_id=user_id).all()
                results = [appointment.to_dict() for appointment in appointments]
                return results, 200
            else:
                # Patients can only see their own appointment by ID
                appointment = Appointment.query.filter_by(id=id, patient_id=user_id).first()
                if appointment is None:
                    return {"message": "Appointment not found or unauthorized"}, 404
                return appointment.to_dict(), 200

        elif jwt['role'] in ['doctor', 'admin']:
            if id is None:
                # Doctors and admins can see all appointments
                appointments = Appointment.query.all()
                results = [appointment.to_dict() for appointment in appointments]
                return results, 200
            else:
                # Doctors and admins can see any appointment by ID
                appointment = Appointment.query.filter_by(id=id).first()
                if appointment is None:
                    return {"message": "Appointment not found"}, 404
                return appointment.to_dict(), 200

        else:
            return {"message": "Unauthorized request"}, 401
    @jwt_required()
    def post(self):
        jwt = get_jwt()
        user_id = get_jwt_identity()

        if jwt['role'] != 'patient':
            return {"message": "Unauthorized request"}, 401

        args = self.parser.parse_args()
        if Appointment.query.filter_by(patient_id=user_id).first():
            return {"message": "Patient already has an appointment"}, 400

        appointment = Appointment(
            reason=args['reason'],
            date_time=args['date_time'],
            patient_id=user_id,
            doctor_id=None  # Assuming you have logic to assign a doctor later
        )

        db.session.add(appointment)
        db.session.commit()

        return appointment.to_dict(), 201


    @jwt_required()
    def patch(self, id):
        jwt = get_jwt()
        if jwt['role'] != 'doctor':
            return {"messgae": "Unauthorized request"}, 401

        data = self.parser.parse_args()
        appointment = Appointment.query.filter_by(id=id).first()

        if appointment == None:
            return {"message": "Appointment not found"}, 404

        appointment = db.session.query(Appointment).first(
            and_(Appointment.timestamp == data['create_at'], not_(Appointment.id == id))).first()

        if appointment:
            return {"message": "Appointment already exists for this timestamp"}, 422

        for key in data.keys():
            setattr(appointment, key, data[key])

            db.session.commit()
            return {"message": "Appointment updated successfully"}

    @jwt_required()
    def delete(self, id):
        jwt = get_jwt()
        if jwt['role'] != 'doctor':
            return {"messgae": "Unauthorized request"}, 401

        appointment = Appointment.query.filter_by(id=id).first()
        if appointment == None:
            return {"message": "Appointment not found"}, 404

        db.session.delete(appointment)
        db.session.commit()
        return {"message": "Appointment deleted successfully"}, 200


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

        if jwt['role'] != 'admin' or jwt['role'] != 'doctor':
            return {"messgae": "Unauthorized request"}, 401

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
    def patch(self, id):
        jwt = get_jwt()
        if jwt['role'] != 'admin':
            return {"message": "Unauthorized request"}, 401

        data = self.parser.parse_args()

        data['password'] = generate_password_hash(
            data['password']).decode('utf-8')

        doctor = Doctor.query.filter_by(id=id).first()

        if doctor == None:
            return {"message": "Doctor not found"}, 404

        email = db.session.query(Doctor).first(
            and_(Doctor.email == data['email'], not_(Doctor.id == id))).first()
        if email:
            return {"message": "Email already exists"}, 422

        phone = db.session.query(Doctor).first(
            and_(Doctor.phone_number == data['phone_number'], not_(Doctor.id == id))).first()

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
            return {"message": "Unauthorized request"}, 401

        doctor = Doctor.query.filter_by(id=id).first()
        if doctor == None:
            return {"message": "Doctor not found", "status": "fail"}, 404

        db.session.delete(doctor)
        db.session.commit()
        return {"message": "Doctor deleted successfully"}


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
        
    

        # if id == None:
        #     patients = Patient.query.all()
        #     results = []

        #     for patient in patients:
        #         results.append(patient.to_dict())

        #     return results
        # else:
        #     patient = Patient.query.filter_by(id=id).first()
        #     if patient == None:
        #         return {"message": "Patient not found"}, 404

        #     return patient.to_dict()

    @jwt_required()
    def post(self):
        jwt = get_jwt()
        if jwt['role'] != 'patient':
            return {"message": "Unauthorized request"}, 401

        data = PatientResource.parser.parse_args()

        data['password'] = generate_password_hash(
            data['password']).decode('utf-8')

        print(data)
        # verify email and phone numbers are available
        email = Patient.query.filter_by(email=data['email']).first()
        if email:
            return {"message": "Email already exists"}, 422

        phone = Patient.query.filter_by(
            phone_number=data['phone_number']).first()
        if phone:
            return {"message": "Phone number already exists"}, 422

        patient = Patient(**data)
        db.session.add(patient)
        db.session.commit()

        return {"message": "Patient created successfully"}

    @jwt_required()
    def delete(self, id):

        jwt = get_jwt()
        if jwt['role'] != 'admin' or jwt['role'] != 'doctor':
            return {"message": "Unauthorized request"}, 401

        patient = Patient.query.filter_by(id=id).first()
        if patient == None:
            return {"message": "Patient not found", "status": "fail"}, 404
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted successfully"}


# from flask_restful import Resource,reqparse
# from models import db, Specialization
# from flask import Flask, jsonify, request, make_response
# from flask_jwt_extended import jwt_required, get_jwt
# from sqlalchemy import and_, not_


class SpecializationResource(Resource):

   # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True,
                        help="Name is required")

    @jwt_required()
    def get(self, id=None):

        jwt = get_jwt()

        if jwt['role'] != 'admin' or jwt['role'] != 'doctor' or jwt['role'] != 'patient':
            return {"messgae": "Unauthorized request"}, 401

        if id == None:
            specializations = Specialization.query.all()
            results = []

            for specialization in specializations:
                results.append(specialization.to_dict())

            return results

        else:
            specialization = Specialization.query.filter_by(id=id).first()

            if specialization == None:
                return {"message": "Specialization not found"}, 404

            return specialization.to_dict()

    @jwt_required()
    def post(self):
        jwt = get_jwt()
        if jwt['role'] != 'admin':
            return {"message": "Unauthorized request"}, 401

        new_record = Specialization(
            name=request.form['name']
        )
        db.session.add(new_record)
        db.session.commit()
        response_dict = new_record.to_dict()
        response = make_response(
            response_dict,
            201)
        return response
