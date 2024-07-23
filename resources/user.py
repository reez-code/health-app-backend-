from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    jwt_required
)
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
from models import db, Doctor, Patient, Admin

bcrypt = Bcrypt()

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
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

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
            return {"error": str(e)}, 500

class LoginResource(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role').lower()

        user = None
        if role == 'patient':
            user = Patient.query.filter_by(email=email).first()
        elif role == 'doctor':
            user = Doctor.query.filter_by(email=email).first()
        elif role == 'admin':
            user = Admin.query.filter_by(email=email).first()
        else:
            return {"message": "Invalid role"}, 400

        if user and bcrypt.check_password_hash(user.password, password):
            additional_claims = {"role": role}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            return {
                "access_token": access_token,
                "message": f"Logged in as {role}"
            }, 200
        else:
            return {"message": "Invalid email or password"}, 401

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        # JWT handles logout by removing the token from the client-side.
        return {"message": "Logged out successfully"}, 200