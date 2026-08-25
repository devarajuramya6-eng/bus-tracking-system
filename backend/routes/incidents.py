"""
CityBus Enterprise Platform - Incidents & Emergency SOS API
File: backend/routes/incidents.py
"""

from flask import Blueprint, request, jsonify
from services.incident_service import IncidentService
from repositories.incident_repository import IncidentRepository

incidents_bp = Blueprint('incidents_v1', __name__, url_prefix='/api/v1/incidents')


@incidents_bp.route('', methods=['GET'])
def get_incidents():
    """Lists incidents with status filter."""
    try:
        status = request.args.get('status')
        incidents = IncidentRepository.get_all_incidents(status)
        return jsonify({
            "success": True,
            "count": len(incidents),
            "incidents": [i.to_dict() for i in incidents]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@incidents_bp.route('', methods=['POST'])
def report_incident():
    """Creates a new incident report."""
    try:
        data = request.get_json() or {}
        inc_type = data.get('incident_type', 'Breakdown')
        title = data.get('title', 'Bus Incident Reported')
        description = data.get('description', '')
        severity = data.get('severity', 'Medium')
        bus_id = data.get('bus_id')
        driver_id = data.get('driver_id')
        route_id = data.get('route_id')
        lat = data.get('latitude')
        lng = data.get('longitude')
        reported_by = data.get('reported_by')

        incident = IncidentService.report_incident(
            incident_type=inc_type,
            title=title,
            description=description,
            severity=severity,
            bus_id=bus_id,
            driver_id=driver_id,
            route_id=route_id,
            lat=lat,
            lng=lng,
            reported_by=reported_by
        )

        return jsonify({
            "success": True,
            "message": "Incident logged successfully",
            "incident": incident.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@incidents_bp.route('/emergency/sos', methods=['POST'])
def trigger_emergency_sos():
    """Triggers high-priority Emergency SOS broadcast (Driver Panic Button)."""
    try:
        data = request.get_json() or {}
        bus_id = data.get('bus_id')
        driver_id = data.get('driver_id')
        lat = data.get('latitude', 16.5062)
        lng = data.get('longitude', 80.6480)
        details = data.get('details', 'Driver pressed emergency SOS panic button')

        incident = IncidentService.trigger_emergency_sos(bus_id, driver_id, lat, lng, details)
        return jsonify({
            "success": True,
            "message": "EMERGENCY SOS BROADCAST ACTIVE",
            "incident": incident.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@incidents_bp.route('/<int:incident_id>/status', methods=['PATCH'])
def update_status(incident_id):
    """Updates Kanban incident status (New -> Acknowledged -> In Progress -> Resolved)."""
    try:
        data = request.get_json() or {}
        status = data.get('status')
        notes = data.get('resolution_notes')
        dispatcher = data.get('dispatcher')

        if not status:
            return jsonify({"success": False, "message": "Missing status"}), 400

        inc = IncidentRepository.update_incident_status(incident_id, status, notes, dispatcher)
        if not inc:
            return jsonify({"success": False, "message": f"Incident {incident_id} not found"}), 404

        return jsonify({
            "success": True,
            "incident": inc.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
