
from flask_restful import Resource,reqparse
from models import db, Specialization
from flask import  request, make_response
from flask_jwt_extended import jwt_required, get_jwt






class SpecializationResource(Resource):
    
   # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('name', required = True,
                        help = "Name is required")
    
    @jwt_required()
    def get(self, id=None):
        
        jwt = get_jwt()
        
        if jwt['role'] == 'admin' or  jwt['role'] == 'doctor' or  jwt['role'] != 'patient':
            
        
            if id ==None:
                specializations = Specialization.query.all()
                results = []
            
                for specialization  in  specializations:
                    results.append(specialization.to_dict())
                    
                return results
        
            else:
                specialization = Specialization.query.filter_by(id=id).first()
                
                if specialization == None:
                    return {"message": "Specialization not found"}, 404
                
                return specialization.to_dict()
        else:
            return {"messgae":"Unauthorized request"}, 401
   
    @jwt_required()
    def post(self):
        jwt = get_jwt()
        if jwt['role'] == 'admin':
            
            new_record = Specialization(
                name=request.form['name']
            )  
            db.session.add(new_record)
            db.session.commit()
            response_dict = new_record.to_dict()
            response = make_response(
                response_dict,
                201)
            return response
        else:
            return {"message":"Unauthorized request"}, 401