from flask_restful import Resource, reqparse 
from models import db, Appointment
from sqlalchemy import and_, not_
from flask_jwt_extended import jwt_required, get_jwt


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
        if jwt['role'] != 'doctor' or jwt['role'] != 'admin':
             return {"messgae":"Unauthorized request"}, 401
        
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
        
     @jwt_required()
     def patch(self, id):
            jwt = get_jwt()
            if jwt['role']!= 'doctor':
                return {"messgae":"Unauthorized request"}, 401
            
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
         
            
        
        
         


# # Appointment Resource
# class AppointmentResource(Resource):
#     def get(self):
#         appointments = Appointment.query.all()
#         appointments_dict = [appointment.to_dict() for appointment in appointments]
#         return jsonify(appointments_dict)

#     def post(self):
#         data = request.get_json()
#         try:
#             timestamp = datetime.fromisoformat(data['timestamp'])
#         except ValueError:
#             return jsonify({"error": "Invalid timestamp format. Use 'YYYY-MM-DDTHH:MM:SS' format."}), 400

#         appointment = Appointment(reason=data['reason'], timestamp=timestamp)
#         db.session.add(appointment)
#         db.session.commit()
#         return jsonify(appointment.to_dict()), 201

# class AppointmentDetailResource(Resource):
#     def patch(self, id):
#         data = request.get_json()
#         appointment = Appointment.query.get(id)
#         if not appointment:
#             return jsonify({"error": "Appointment not found"}), 404

#         if 'reason' in data:
#             appointment.reason = data['reason']
#         if 'timestamp' in data:
#             try:
#                 timestamp = datetime.fromisoformat(data['timestamp'])
#             except ValueError:
#                 return jsonify({"error": "Invalid timestamp format. Use 'YYYY-MM-DDTHH:MM:SS' format."}), 400
#             appointment.timestamp = timestamp

#         db.session.commit()
#         return jsonify(appointment.to_dict()), 200

#     def delete(self, id):
#         appointment = Appointment.query.get(id)
#         if appointment is None:
#             return jsonify({"error": "Appointment not found."}), 404

#         db.session.delete(appointment)
#         db.session.commit()
#         return jsonify({"message": "Appointment deleted successfully."}), 200