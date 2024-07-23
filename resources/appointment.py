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
     
     @jwt_required()
     def post(self):
        jwt = get_jwt()
        # Only allow doctors and admins to create appointments
        if jwt['role'] != 'doctor' and jwt['role'] != 'admin' and jwt['role'] != 'patient':
            return {"message": "Unauthorized request"}, 401

        # Parse the request data
        data = self.parser.parse_args()

        # Check if an appointment with the same timestamp already exists
        existing_appointment = Appointment.query.filter_by(date_time=data['date_time']).first()
        if existing_appointment:
            return {"message": "An appointment already exists for this timestamp"}, 422

        # Create a new Appointment instance
        new_appointment = Appointment(
            reason=data['reason'],
            date_time=data['date_time'],
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id']
        )

        # Add the new appointment to the database
        try:
            db.session.add(new_appointment)
            db.session.commit()
            return {"message": "Appointment created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500


class AppointmentIDResource(Resource):
     def get (self, appointment_id):
         appointment = Appointment.query.filter_by(id=appointment_id).first()
         
         if appointment is None:
             return {"messgae": "Appointment not found"}, 404
         
         patients =[]
         
         for patient in appointment.patients:
             patients.append(patient.to_dict())
             
             return patients

         
         
            
        
        
         
