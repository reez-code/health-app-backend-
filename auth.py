
from flask import Blueprint, request, jsonify, session
from modelss import  Appointment, Doctor, Patient, Admin
#from app import app
from werkzeug.security import check_password_hash


auth_bp = Blueprint('auth', __name__)


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
        session['username'] = username
        session['role'] = role
        return jsonify({"message": f"Logged in as {role}"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


# Logout route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/signup/patient', methods=['POST'])
def signup_patient():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not all([name, email, password]):
        return jsonify({"message": "Missing data"}), 400

    hashed_password = generate_password_hash(password)
    new_patient = Patient(name=name, email=email, password=hashed_password)
    
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({"message": "Patient created successfully"}), 201
