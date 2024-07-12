from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
import validators
from sqlalchemy.orm import validates

db=SQLAlchemy()

class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    specialization = db.Column(db.String)
    password=db.Column(db.String)
    image=db.Column(db.String)
    
    def to_dict(self):
        return {"id": self.id,
                "name": self.name, 
                "email": self.email,
                "phone": self.phone,
                "specialization": self.specialization, 
                "image": self.image}
    
    
    # patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    # patients = db.relationship("Patient", back_populates="doctor")
    ''' departments = db.relationship("Department", secondary="doc_department",
                                back_populates="doctors")'''

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
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {"id": self.id,
                "reason": self.reason, 
                "timestamp": self.timestamp}

    @validates("timestamp")
    def validate_timestamp(self, key, timestamp):
        if not isinstance(timestamp, datetime):
            raise ValueError("Timestamp must be a datetime object")
        return timestamp

    def __repr__(self):
        return f"Appointment(id={self.id}, reason={self.reason}, timestamp={self.timestamp})"


class Admin(db.Model, SerializerMixin):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    password=db.Column(db.String)
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
    
class Signup(db.Model,SerializerMixin):
        __tablename__ ='signups'
        id = db.Column(db.Integer, primary_key=True)
        name=db.Column(db.String,nullable=False)
        email = db.Column(db.String, nullable=False, unique=True)
        password = db.Column(db.String, nullable=False)
        
        
        def to_dict(self):
            return {
                'id': self.id,
                "name": self.name,
                'email': self.email,
            
            }
        
        @validates('email')
        def validate_email(self, key, email):
            if not validators.email(email):
                raise ValueError("Invalid email address")
            return email
        
  

def __repr__(self):
        return f"Admin(id={self.id}, name={self.name}, email={self.email})"
