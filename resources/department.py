
from flask_restful import Resource,reqparse
from models import db, Department
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_, not_





class DepartmentResource(Resource):
    
   # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('name', required = True,
                        help = "Name is required")
    
    @jwt_required()
    def get(self, id=None):
        
        jwt = get_jwt()
        
        if jwt['role'] != 'admin' or  jwt['role'] != 'doctor' or  jwt['role'] != 'patient':
            return {"messgae":"Unauthorized request"}, 401
        
        if id ==None:
            departments = Department.query.all()
            results = []
        
            for department in  departments:
                results.append(department.to_dict())
                
            return results
    
        else:
            department = Department.query.filter_by(id=id).first()
            
            if department == None:
                return {"message": "Department not found"}, 404
            
            return department.to_dict()
        
   
    @jwt_required()
    def post(self):
        jwt = get_jwt()
        if jwt['role'] != 'admin':
            return {"message":"Unauthorized request"}, 401
        

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