import os
from resources import DoctorResource, AppointmentResource,AdminResource, SignupResource,SpecializationResource,PatientResource
from auth import LoginResource,LogoutResource
from flask import Flask, make_response
from flask_migrate import Migrate
from flask_restful import Api,Resource
from models import db
import secrets
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


#from auth import auth_bp  



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set a secret key for session management
#app.config['SECRET_KEY'] = secrets.token_hex(16) # Change this to a random, unique string

app.config['JWT_SECRET_KEY'] = "hospitalmanagement_secret"
# Access tokens should be short lived, this is for this phase only
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db.init_app(app)
migrate = Migrate(app, db)


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
api.add_resource(DoctorResource, '/doctors', '/doctors/<int:id>')
# api.add_resource(DoctorDetailResource, '/doctors/<int:id>')
api.add_resource(AppointmentResource, '/appointments', '/appointments/<int:id>')
# api.add_resource(AppointmentDetailResource, ')
api.add_resource(AdminResource, '/admins')
api.add_resource(SignupResource, '/signup')
#api lema
api.add_resource(SpecializationResource, '/specializations_all')

api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')



#app.register_blueprint(auth_bp, url_prefix='/auth')








if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True ,port=5555)
