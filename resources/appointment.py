from flask_restful import Resource
from models import db, Appointment
from flask import Flask, jsonify, request, make_response
from datetime import datetime



# Appointment Resource
class AppointmentResource(Resource):
    def get(self):
        appointments = Appointment.query.all()
        appointments_dict = [appointment.to_dict() for appointment in appointments]
        return jsonify(appointments_dict)

    def post(self):
        data = request.get_json()
        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except ValueError:
            return jsonify({"error": "Invalid timestamp format. Use 'YYYY-MM-DDTHH:MM:SS' format."}), 400

        appointment = Appointment(reason=data['reason'], timestamp=timestamp)
        db.session.add(appointment)
        db.session.commit()
        return jsonify(appointment.to_dict()), 201

class AppointmentDetailResource(Resource):
    def patch(self, id):
        data = request.get_json()
        appointment = Appointment.query.get(id)
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        if 'reason' in data:
            appointment.reason = data['reason']
        if 'timestamp' in data:
            try:
                timestamp = datetime.fromisoformat(data['timestamp'])
            except ValueError:
                return jsonify({"error": "Invalid timestamp format. Use 'YYYY-MM-DDTHH:MM:SS' format."}), 400
            appointment.timestamp = timestamp

        db.session.commit()
        return jsonify(appointment.to_dict()), 200

    def delete(self, id):
        appointment = Appointment.query.get(id)
        if appointment is None:
            return jsonify({"error": "Appointment not found."}), 404

        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"message": "Appointment deleted successfully."}), 200