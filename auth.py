
from flask import Blueprint, request, jsonify, session
from models import User, Appointment, Doctor, Patient
#from app import app
from werkzeug.security import check_password_hash


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['username'] = username
        session['role'] = user.role
        return jsonify({"message": f"Logged in as {user.role}"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# Logout route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return jsonify({"message": "Logged out successfully"}), 200

#Route to access appointments
@auth_bp.route('/appointments', methods=['GET'])
def get_appointments():
    if 'role' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    
    role = session['role']
    if role == 'patient':
        patient = Patient.query.filter_by(name=session['username']).first()
        if not patient:
            return jsonify({"message": "Patient not found"}), 404
        appointments = Appointment.query.filter_by(patient_id=patient.id).all()
        return jsonify({"appointments": [app.to_dict() for app in appointments]}), 200

    elif role == 'doctor':
        doctor = Doctor.query.filter_by(name=session['username']).first()
        if not doctor:
            return jsonify({"message": "Doctor not found"}), 404
        appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
        return jsonify({"appointments": [app.to_dict() for app in appointments]}), 200

    elif role == 'admin':
        appointments = Appointment.query.all()
        return jsonify({"appointments": [app.to_dict() for app in appointments]}), 200

    return jsonify({"message": "Unauthorized"}), 401

# Route for viewing doctors (admin only)
@auth_bp.route('/doctors', methods=['GET'])
def get_doctors():
    if 'role' not in session or session['role'] not in ['admin', 'patient']:
        return jsonify({"message": "Unauthorized"}), 401

    doctors = Doctor.query.all()
    return jsonify({"doctors": [doc.to_dict() for doc in doctors]}), 200

# Route for viewing patients (doctor and admin only)
@auth_bp.route('/patients', methods=['GET'])
def get_patients():
    if 'role' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    
    role = session['role']
    if role == 'doctor' or role == 'admin':
        patients = Patient.query.all()
        return jsonify({"patients": [pat.to_dict() for pat in patients]}), 200

    return jsonify({"message": "Unauthorized"}), 401

