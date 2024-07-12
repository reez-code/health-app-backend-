from resources import DoctorResource, DoctorDetailResource, AppointmentResource, AppointmentDetailResource, AdminResource, SignupResource
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from models import db
import logging


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

logging.basicConfig(level=logging.DEBUG)


# Add resources to API
api.add_resource(DoctorResource, '/doctors')
api.add_resource(DoctorDetailResource, '/doctors/<int:id>')
api.add_resource(AppointmentResource, '/appointments')
api.add_resource(AppointmentDetailResource, '/appointments/<int:id>')
api.add_resource(AdminResource, '/admins')
api.add_resource(SignupResource, '/signup')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
