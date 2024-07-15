#!/usr/bin/env python3

from flask import Flask
from flask_migrate import Migrate
from datetime import datetime
from flask_restful import Api, Resource
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from flask_bcrypt import generate_password_hash,Bcrypt
from sqlalchemy import and_, not_


from models import db
# from server.models import db, Department,Patient,Doctor,Appointment,Admin 
from resources.patient import PatientResource
from resources.department import DepartmentResource
from resources.doctor import DoctorResource, DoctorDetailResource
from resources.admin import AdminResource
from resources.appointment import AppointmentResource, AppointmentDetailResource




app = Flask(__name__)
# configure db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"


migrate = Migrate(app, db)

# setup migration tool
db.init_app(app)

api = Api(app)

# initialize bcrypt
bcrypt = Bcrypt(app)

# setup jwt
jwt = JWTManager(app)



class Home(Resource):

    def get(self):

        response_dict = {
            "message": "Welcome to the Health Application",
        }

        response = make_response(
            response_dict,
            200
        )

        return response

# Add resources to API
api.add_resource(Home, '/')         
api.add_resource(PatientResource,'/patients','/patients/<int:id>')
api.add_resource(DepartmentResource, '/departments_all')
api.add_resource(DoctorResource, '/doctors')
api.add_resource(DoctorDetailResource, '/doctors/<int:id>')
api.add_resource(AppointmentResource, '/appointments')
api.add_resource(AppointmentDetailResource, '/appointments/<int:id>')
api.add_resource(AdminResource, '/admins')
# api.add_resource(SignupResource, '/signup')
# api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(port=5000, debug=True)