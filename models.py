from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import validators
from werkzeug.security import generate_password_hash, check_password_hash
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

class Department(db.Model, SerializerMixin):
    __tablename__ = "departments"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    
    def __repr__(self):
        return f"<Category {self.id}: {self.name}>"
    

    
class Patient(db.Model, SerializerMixin):
    __tablename__= "patients"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    gender = db.Column(db.String,nullable=False)
    age = db.Column(db.String,nullable=False)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    diagnosis=db.Column(db.String,nullable=False)
    password = db.Column(db.String, nullable=False)
    # appointment_id=db.Column(db.Integer, db.ForeignKey('appointments.id'))
    
    
    
    @validates("phone")
    def validate_phone(self,key,phone):
        if not validators.length(phone, min=10, max=15):
            raise ValueError("Phone number must be between 10 and 15 characters")
        return phone
        
        
    def validate_email(self, key, email):
        # Simple regex for validating an Email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email
    
    
    
    def __repr__(self):
        return f"<Admin {self.name},{self.gender},{self.age},{self.phone_number},{self.email}>"
    
class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=False)
    specialization = db.Column(db.String, nullable=False)
    password=db.Column(db.String, nullable=False)
    image=db.Column(db.String)
    
    
    # patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    # patients = db.relationship("Patient", back_populates="doctor")
    ''' departments = db.relationship("Department", secondary="doc_department",
                                back_populates="doctors")'''

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
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # def to_dict(self):
    #     return {"id": self.id,
    #             "reason": self.reason, 
    #             "timestamp": self.timestamp}

    # @validates("timestamp")
    # def validate_timestamp(self, key, timestamp):
    #     if not isinstance(timestamp, datetime):
    #         raise ValueError("Timestamp must be a datetime object")
    #     return timestamp

    def __repr__(self):
        return f"<Appointment {self.id}:{self.reason},{self.created_at}>"


class Admin(db.Model, SerializerMixin):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=False)
    password=db.Column(db.String)
    



    def validate_email(self, key, email):
        # Simple regex for validating an Email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email

    # @validates('phone')
    # def validate_phone(self, key, phone):
    #     if not validators.length(phone, min=10, max=15):
    #         raise ValueError("Phone number must be between 10 and 15 characters")
    #     return phone
    
    def __repr__(self):
        return f"<Appointment {self.id}:{self.name},{self.email},{self.phone_number},{self.password}>"
        
  

def __repr__(self):
        return f"Admin(id={self.id}, name={self.name}, email={self.email})"
    
    
    
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.Text)
    password = db.Column(db.String)

    serialize_rules = ('-password',)

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)
    
    
