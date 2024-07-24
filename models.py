from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_bcrypt import check_password_hash
import re

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# initialize metadata
metadata = MetaData(naming_convention = convention)

# initialize db instance with metadata and engine
db = SQLAlchemy(metadata=metadata)

# many to many relationship
doctor_specialization_association = db.Table(
    'doctor_specialization_association',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctors.id'), primary_key=True),
    db.Column('specialization_id', db.Integer, db.ForeignKey('specializations.id'), primary_key=True)
)

class Specialization(db.Model, SerializerMixin):
    __tablename__ = "specializations"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    doctors = db.relationship('Doctor', secondary=doctor_specialization_association, back_populates='specializations')

    serialize_rules = ('-doctors.specializations',)
    
    
    def __repr__(self):
        return f"<Specialization {self.id}: {self.name}>"
    

    
class Patient(db.Model, SerializerMixin):
    __tablename__= "patients"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.String)
    phone_number = db.Column(db.String, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    diagnosis=db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    # appointment_id=db.Column(db.Integer, db.ForeignKey('appointments.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    
    doctor = db.relationship('Doctor', back_populates= 'patients')
    appointments = db.relationship("Appointment",uselist= False, back_populates="patient")
    
    serialize_rules = ('-password', '-doctor.patients', '-appointments.patient',)

        
        
    def validate_email(self, key, email):
        # Simple regex for validating an Email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'doctor_id': self.doctor_id,
            'phone_number': self.phone_number,
            'email': self.email,
            'diagnosis': self.diagnosis
        }
    def __repr__(self):
        return f"<Patient {self.name},{self.email}>"
    
class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String)
    password=db.Column(db.String, nullable=False)
    image=db.Column(db.String)
   
    # patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    # appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"))
    
    patients = db.relationship("Patient", back_populates="doctor")
    appointments = db.relationship("Appointment", back_populates="doctor")
    
    specializations = db.relationship("Specialization", secondary="doctor_specialization_association",
                                  back_populates="doctors")
    serialize_rules = ('-password', '-patients.doctor', '-appointments.doctor', '-specializations.doctors',)

    def validate_email(self, key, email):
        # Simple regex for validating an Email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email


    def __repr__(self):
        return f"<{self.id}, {self.name}, {self.email}, {self.email}, {self.phone_number}, {self.specialization}, {self.password}, {self.image}>"


class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    
    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")
    
    serialize_rules = ('-patient.appointments', '-doctor.appointments',)

    def __repr__(self):
        return f"<Appointment {self.id}:{self.reason},{self.date_time},{self.patient_id},{self.doctor_id}>"


class Admin(db.Model, SerializerMixin):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String)
    password=db.Column(db.String)
    

    serialize_rules = ('-password',)

    def validate_email(self, key, email):
        # Simple regex for validating an Email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email
    
 


def __repr__(self):
        return f"Admin(id={self.id},{self.name},{self.email},{self.phone_number},{self.password})"
    
    
    
# class User(db.Model, SerializerMixin):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text, nullable=False)
#     email = db.Column(db.String, nullable=False, unique=True)
#     role = db.Column(db.Text)
#     password = db.Column(db.String)

#     serialize_rules = ('-password',)

#     def check_password(self, plain_password):
#         return check_password_hash(self.password, plain_password)
    
    
