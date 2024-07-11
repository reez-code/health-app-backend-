# from flask import Flask ,request
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from app import app


# app = Flask(__name__)
# app.config["SQLALCHEMY DATABASE URI"]="sqlite:///test.db"

# db=SQLAlchemy(app)
# migrate=Migrate(app,db)

# from models import Doctor,Appointment,Admin

# @app.route("/doctors", methods=["GET"])
# def get_doctors():
#     if request.method == "GET":
#         doctors= Doctor.query.all()
#         return[doctor.to_dict() for doctor in doctors]
    
    
#     if request.method == "POST":
#         data=request.get_json()
#         doctor=Doctor(name=data['name'], email=data['email'], phone=data['phone'], specialization=data['specialization'],image=data['image'])
#         db.session.add(doctor)
#         db.session.commit()
#         return doctor.get_doctors(), 201
    
   
        
        