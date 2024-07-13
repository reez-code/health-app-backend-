from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship

db = SQLAlchemy()


doctor_department_association = db.Table(
    'doctor_department_association',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctors.id'), primary_key=True),
    db.Column('department_id', db.Integer, db.ForeignKey('departments.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)   # 'patient', 'doctor', 'admin'
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {"id": self.id,
                "username": self.name,
                "email": self.email,
                "password": self.password,
                "role": self.role}

class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    specialization = db.Column(db.String)
    password = db.Column(db.String)
    image = db.Column(db.String)

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "phone": self.phone,
                "specialization": self.specialization,
                "image": self.image}

    patients = db.relationship("Patient", back_populates="doctor")
    appointments = db.relationship("Appointment", back_populates="doctor")
    departments = db.relationship("Department", secondary="doctor_department_association",
                                  back_populates="doctors")

    @validates("email")
    def validate_email(self, key, email):
        if not validators.email(email):
            raise ValueError("Invalid email address")
        return email

    # @validates("phone")
    # def validate_phone(self, key, phone):
    #     if not validators.length(phone, min=10, max=15):
    #         raise ValueError("Phone number must be between 10 and 15 characters")
    #     return phone

    def __repr__(self):
        return f"Doctor(id={self.id}, name={self.name}, email={self.email})"


class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id,
                "reason": self.reason,
                "patient_id": self.patient_id,
                "doctor_id": self.doctor_id,
                "timestamp": self.timestamp}

    @validates("timestamp")
    def validate_timestamp(self, key, timestamp):
        if not isinstance(timestamp, datetime):
            raise ValueError("Timestamp must be a datetime object")
        return timestamp

    doctor = db.relationship("Doctor", back_populates="appointments")
    patient = db.relationship("Patient", back_populates="appointment")

    def __repr__(self):
        return f"Appointment(id={self.id}, reason={self.reason}, timestamp={self.timestamp})"


class Admin(db.Model, SerializerMixin):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role
        }

    @validates('email')
    def validate_email(self, key, email):
        if not validators.email(email):
            raise ValueError("Invalid email address")
        return email

    # @validates('phone')
    # def validate_phone(self, key, phone):
    #     if not validators.length(phone, min=10, max=15):
    #         raise ValueError("Phone number must be between 10 and 15 characters")
    #     return phone


# class Signup(db.Model, SerializerMixin):
#     __tablename__ = 'signups'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, nullable=False)
#     email = db.Column(db.String, nullable=False, unique=True)
#     password = db.Column(db.String, nullable=False)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             "name": self.username,
#             'email': self.email,

#         }

#     @validates('email')
#     def validate_email(self, key, email):
#         if not validators.email(email):
#             raise ValueError("Invalid email address")
#         return email

# lema code


class Department(db.Model, SerializerMixin):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    doctors = db.relationship("Doctor", secondary="doctor_department_association",
                              back_populates="departments")

    def to_dict(self):
        return {"id": self.id,
                "name": self.name
                }


class Patient(db.Model, SerializerMixin):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    age = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String)
    diagnosis = db.Column(db.String)
    password = db.Column(db.String)
    # appointment_id=db.Column(db.Integer, db.ForeignKey('appointments.id'))

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "gender": self.gender,
                "phone_number": self.phone_number,
                "diagnosis": self.diagnosis,
                "email": self.email,
                "password": self.password,
                "doctor_id": self.doctor_id,
                "age": self.age,
                }
    doctor = db.relationship("Doctor", back_populates="patients")
    appointment = db.relationship(
        "Appointment", uselist=False, back_populates="patient")

    @validates("phone")
    def validate_phone(self, key, phone):
        if not validators.length(phone, min=10, max=15):
            raise ValueError(
                "Phone number must be between 10 and 15 characters")
        return phone

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Failed simple email validation")
        return address


def __repr__(self):
    return f"Admin(id={self.id}, name={self.name}, email={self.email})"
