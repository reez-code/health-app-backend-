from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import validators
from sqlalchemy.orm import validates

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Department(db.Model, SerializerMixin):
    __tablename__ = "departments"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    

    
class Patient(db.Model, SerializerMixin):
    __tablename__= "patients"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String)
    diagnosis=db.Column(db.String)
    password = db.Column(db.String)
    # appointment_id=db.Column(db.Integer, db.ForeignKey('appointments.id'))
    
    
    
    @validates("phone")
    def validate_phone(self,key,phone):
        if not validators.length(phone, min=10, max=15):
            raise ValueError("Phone number must be between 10 and 15 characters")
        return phone
        
        
    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Failed simple email validation")
        return address
    
    def __repr__(self):
        return f"<Admin {self.name},{self.gender},{self.age},{self.phone_number},{self.email}>"
    
    
    
    
    
    
