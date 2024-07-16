from resources import DoctorResource, DoctorDetailResource, AppointmentResource, AppointmentDetailResource, AdminResource, SignupResource, Home,Patients,PatientByID,DepartmentResource
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from modelss import db
from auth import auth_bp  
import logging


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set a secret key for session management
app.config['SECRET_KEY'] = 'secrets.token_hex(16)' # Change this to a random, unique string



db.init_app(app)
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
api.add_resource(DoctorResource, '/doctors', '/doctors/<int:id>')
# api.add_resource(DoctorDetailResource, '/doctors/<int:id>')
api.add_resource(AppointmentResource, '/appointments', '/appointments/<int:id>')
# api.add_resource(AppointmentDetailResource, ')
api.add_resource(AdminResource, '/admins')
api.add_resource(SignupResource, '/signup')
#api lema
api.add_resource(DepartmentResource, '/departments_all')
api.add_resource(Patients, '/patients')
api.add_resource(PatientByID, '/patients/<int:id>')
api.add_resource(Home, '/')



app.register_blueprint(auth_bp, url_prefix='/auth')








if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
