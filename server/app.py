#!/usr/bin/env python3

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy  import SQLAlchemy
from flask_restful import Api, Resource
from flask import Flask, jsonify, request, make_response

from models import db, Department,Patient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)



class Home(Resource):

    def get(self):

        response_dict = {
            "message": "Welcome to the Welcome to Health Application",
        }

        response = make_response(
            response_dict,
            200
        )

        return response

api.add_resource(Home, '/')

class Patients(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Patients.querry.all()]
        response = make_response(
            response_dict_list,
            200)
        return response
        
    
api.add_resource(Departments, '/departments')

if __name__ == '__main__':
    app.run(port=5555, debug=True)