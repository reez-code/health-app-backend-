
from flask_restful import Resource
from models import db, Department
from flask import Flask, jsonify, request, make_response




class DepartmentResource(Resource):
    def get(self):
        results = []
        
        for department in Department.query.all():
            results.append(department.to_dict())
            
        return make_response(jsonify(results), 200)
   
   
    def post(self):

        new_record = Department(
            name=request.form['name']
        )  
        db.session.add(new_record)
        db.session.commit()
        response_dict = new_record.to_dict()
        response = make_response(
            response_dict,
            201)
        return response