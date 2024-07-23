#!/usr/bin/env python3
import os
from datetime import timedelta  
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask import Flask,make_response
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt



from models import db
from resources.patient import PatientResource
from resources.specialization import SpecializationResource
from resources.doctor import DoctorResource
from resources.admin import AdminResource
from resources.appointment import AppointmentResource, AppointmentIDResource
from resources.user import  SignupResource, LoginResource, LogoutResource




app = Flask(__name__)
# configure db connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['JWT_SECRET_KEY'] = "hospitalmanagement_secret"
# Access tokens should be short lived, this is for this phase only
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)


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
api.add_resource(SpecializationResource, '/specializations')
api.add_resource(DoctorResource, '/doctors', '/doctors/<int:id>')
api.add_resource(AppointmentResource, '/appointments', '/appointments/<int:id>')
api.add_resource(AppointmentIDResource, '/appointments/<int:appointment_id>/patients')
api.add_resource(AdminResource, '/admins')
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')

if __name__ == '__main__':
    app.run( debug=True)