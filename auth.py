from flask import jsonify, request
from flask_restful import Resource, Api
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from flask_bcrypt import check_password_hash
from models import Doctor, Patient, Admin

class LoginResource(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        role = data.get('role').lower()

        user = None
        if role == 'patient':
            user = Patient.query.filter_by(name=username).first()
        elif role == 'doctor':
            user = Doctor.query.filter_by(name=username).first()
        elif role == 'admin':
            user = Admin.query.filter_by(name=username).first()
        else:
            return {"message": "Invalid role"}, 400

        if user and check_password_hash(user.password, password):
            additional_claims = {"role": role}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "message": f"Logged in as {role}"
            }, 200
        else:
            return {"message": "Invalid username or password"}, 401

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        # JWT handles logout by removing the token from the client-side.
        return {"message": "Logged out successfully"}, 200


