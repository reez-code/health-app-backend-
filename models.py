from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import validators
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


doctor_specialization_association = db.Table(
    'doctor_specialization_association',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctors.id'), primary_key=True),
    db.Column('specialization_id', db.Integer, db.ForeignKey('specializations.id'), primary_key=True)
)

class Specialization(db.Model, SerializerMixin):
    __tablename__ = "specializations"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    
    doctors = db.relationship("Doctor", secondary="doctor_specialization_association",
                              back_populates="specializations")
    
    doctor_names = association_proxy('doctors', 'name')
    
    
    def __repr__(self):
        return f"<Specialization {self.id}: {self.name}>"
    

    
class Patient(db.Model, SerializerMixin):
    __tablename__= "patients"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    gender = db.Column(db.String,nullable=False)
    age = db.Column(db.String,nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    phone_number = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    diagnosis=db.Column(db.String,nullable=False)
    password = db.Column(db.String, nullable=False)
   
    doctor = db.relationship("Doctor", back_populates="patients")
    appointment = db.relationship(
        "Appointment", uselist=False, back_populates="patient")
    
    
    
        
        
    def validate_email(self, key, email):
        # Simple regex for validating an Email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email
    
    
    
    def __repr__(self):
        return f"<Admin {self.name},{self.email}>"
    
class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=False)
    password=db.Column(db.String, nullable=False)
    image=db.Column(db.String)
    
    
    patients = db.relationship("Patient", back_populates="doctor")
    appointments = db.relationship("Appointment", back_populates="doctor")
    specializations = db.relationship("Specialization", secondary="doctor_specialization_association",
                                  back_populates="doctors")
    
    specialization_names = association_proxy('specializations', 'name')


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
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    date_time = db.Column(db.DateTime, nullable=False)
    #created_at = db.Column(db.DateTime, default=db.func.now())
    
    # def to_dict(self):
    #     return {"id": self.id,
    #             "reason": self.reason, 
    #             "timestamp": self.timestamp}

    # @validates("timestamp")
    # def validate_timestamp(self, key, timestamp):
    #     if not isinstance(timestamp, datetime):
    #         raise ValueError("Timestamp must be a datetime object")
    #     return timestamp
    
    doctor = db.relationship("Doctor",back_populates="appointments")
    patient = db.relationship("Patient", back_populates="appointment")

    def __repr__(self):
        return f"<Appointment(id={self.id}, reason={self.reason}, date_time={self.date_time})>"


class Admin(db.Model, SerializerMixin):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    role = db.Column(db.String)
    



    def validate_email(self, key, email):
        # Simple regex for validating an Email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email

  
    
    def __repr__(self):
        return f"<Appointment {self.id}:{self.name},{self.email},{self.phone_number},{self.password}>"
        
  

def __repr__(self):
        return f"Admin(id={self.id}, name={self.name}, email={self.email})"
    
    
    

    
    
