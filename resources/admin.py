from flask_restful import Resource,reqparse
from models import  Admin
from flask_jwt_extended import jwt_required, get_jwt


# Admin Resource
class AdminResource(Resource):
     # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help="Name is required")
    parser.add_argument('email', required=True, help="Email is required")
    parser.add_argument('phone_number', required=True, help="Phone number is required")
    parser.add_argument('password', required=True, help="Password is required")
    
    @jwt_required()
    def get(self, id=None):
        jwt = get_jwt()
        if jwt['role'] == 'admin':
             
            if id==None:
                admins = Admin.query.all()
                results = []
                
                for admin in admins:
                    results.append(admin.to_dict())
                    
                    return results
            else:
                admin =Admin.query.filter_by(id=id).first()
                
                if admin == None:
                    return {"message": "Admin not found"}, 404
                return admin.to_dict()
        else:
            return {"messgae":"Unauthorized request"}, 401
            
        
   
