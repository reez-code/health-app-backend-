from flask_restful import Resource, reqparse 
from models import db, Appointment
from sqlalchemy import and_, not_
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity


class AppointmentResource(Resource):
     # create a new instance of reqparse
     parser = reqparse.RequestParser()
     parser.add_argument('reason', required=True, 
                         help="Reason is required")
     parser.add_argument('create_at', required=True, 
                         help="Timestamp is required in ISO 8601 format")
     
     @jwt_required()
     def get(self, id=None):
        jwt = get_jwt()
        
        user_identity = get_jwt_identity()
        
        if jwt['role'] == 'doctor' or jwt['role'] == 'admin':
             
            if id == None:
                appointments = Appointment.query.all()
                results = []
                
                for appointment in appointments:
                    results.append(appointment.to_dict())
                    
                return results
            else:
                appointment = Appointment.query.filter_by(id=id).first()
                if appointment is None:
                    return {"messgae": "Appointment not found"}, 404
                return appointment.to_dict()
                        
        else:
            return {"messgae":"Unauthorized request"}, 401
        

        
     @jwt_required()
     def patch(self, id):
            jwt = get_jwt()
            if jwt['role']== 'doctor':
                
            
                data = self.parser.parse_args()
                appointment = Appointment.query.filter_by(id=id).first()
                
                if appointment == None:
                    return {"message": "Appointment not found"}, 404
                
                appointment= db.session.query(Appointment).first(
                    and_(Appointment.timestamp == data['create_at'], not_(Appointment.id==id))).first()
                
                if appointment:
                    return {"message": "Appointment already exists for this timestamp"}, 422

                for key in data.keys():
                    setattr(appointment, key, data[key])
                    
                    db.session.commit()
                    return {"message": "Appointment updated successfully"}
            else:
                return {"messgae":"Unauthorized request"}, 401
            
            
     @jwt_required()
     def delete(self, id):
         jwt = get_jwt()
         if jwt['role']!= 'doctor':
             return {"messgae":"Unauthorized request"}, 401
         
         appointment = Appointment.query.filter_by(id=id).first()
         if appointment == None:
             return {"message": "Appointment not found"}, 404
         
         db.session.delete(appointment)
         db.session.commit()
         return {"message": "Appointment deleted successfully"}, 200
     
class AppointmentIDResource(Resource):
     def get (self, appointment_id):
         appointment = Appointment.query.filter_by(id=appointment_id).first()
         
         if appointment is None:
             return {"messgae": "Appointment not found"}, 404
         
         patients =[]
         
         for patient in appointment.patients:
             patients.append(patient.to_dict())
             
             return patients
         
         
            
        
        
         
