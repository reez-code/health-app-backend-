# #!/usr/bin/env python3

# from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy  import SQLAlchemy
# from flask_restful import Api, Resource
# from flask import Flask, jsonify, request, make_response

# from models import db, Department,Patient

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# migrate = Migrate(app, db)
# db.init_app(app)

# api = Api(app)



# class Home(Resource):

#     def get(self):

#         response_dict = {
#             "message": "Welcome to the Welcome to Health Application",
#         }

#         response = make_response(
#             response_dict,
#             200
#         )

#         return response

# api.add_resource(Home, '/')

# class Patients(Resource):
#     def get(self):
#         response_dict_list = [n.to_dict() for n in Patient.query.all()]
#         response = make_response(
#             response_dict_list,
#             200)
#         return response
    
#     def post(self):
#         new_record = Patient(
#             name=request.form['name'],
#             age=request.form['age'],
#             gender=request.form['gender'],
#             phone_number=request.form['phone_number'],
#             diagnosis=request.form['diagnosis'],
#             email=request.form['email']
#         )
#         db.session.add(new_record)
#         db.session.commit()
#         response_dict = new_record.to_dict()
        
#         response = make_response(
#             response_dict,
#             201)
#         return response
    
# api.add_resource(Patients, '/patients')

# class PatientByID(Resource):
#     def get(self, id):
#         response_dict = Patient.query.filter_by(id=id).first().to_dict()
#         response= make_response(response_dict, 200)
#         return response
    
#     def delete(self,id):
#         record = Patient.query.filter_by(id=id).first()
#         if record:
#             db.session.delete(record)
#             db.session.commit()
#             response_dict = {"message": "Patient deleted successfully"}
#             response = make_response(response_dict, 200)
#         else:
#             response_dict = {"message": "Patient not found"}
#             response = make_response(response_dict, 404)
#         return response

# api.add_resource(PatientByID, '/patients/<int:id>')

# class DepartmentResource(Resource):
#     def get(self):
#         results = []
        
#         for department in Department.query.all():
#             results.append(department.to_dict())
            
#         return make_response(jsonify(results), 200)
   
   
#     def post(self):

#         new_record = Department(
#             name=request.form['name']
#         )  
#         db.session.add(new_record)
#         db.session.commit()
#         response_dict = new_record.to_dict()
#         response = make_response(
#             response_dict,
#             201)
#         return response
    
# api.add_resource(DepartmentResource, '/departments_all')

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)