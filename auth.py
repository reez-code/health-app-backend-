from flask import Blueprint, request, jsonify
from models import Doctor, Patient, Admin
import secrets
from flask_bcrypt import check_password_hash
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity, 
    JWTManager
)

auth_bp = Blueprint('auth', __name__)

# Configure JWT
# def init_jwt(app):
#     app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)  # Change this to your secret key
#     JWTManager(app)

@auth_bp.route('/login', methods=['POST'])
def login():
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
        return jsonify({"message": "Invalid role"}), 400

    if user and check_password_hash(user.password, password):
        additional_claims = {"role": role}
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": f"Logged in as {role}"
        }), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # JWT handles logout by removing the token from the client-side.
    return jsonify({"message": "Logged out successfully"}), 200
