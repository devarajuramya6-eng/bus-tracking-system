"""
CityBus Enterprise Platform - Emergency CAD Dispatch API
File: backend/routes/emergency_dispatch.py

Provides direct integration with 108 emergency first responders.
"""

from flask import Blueprint, request, jsonify
from services.emergency_response_dispatch_service import EmergencyResponseDispatchService

emergency_dispatch_bp = Blueprint('emergency_dispatch_v1', __name__, url_prefix='/api/v1/emergency-dispatch')


@emergency_dispatch_bp.route('/cad-notify', methods=['POST'])
def notify_cad():
    """Dispatches CAD emergency payload."""
    try:
        data = request.get_json() or {}
        incident_id = int(data.get('incident_id', 1))
        bus_id = int(data.get('bus_id', 1))
        e_type = data.get('emergency_type', 'Medical Emergency')
        lat = float(data.get('latitude', 16.5062))
        lng = float(data.get('longitude', 80.6480))
        notes = data.get('notes', 'Driver requested urgent assistance')

        res = EmergencyResponseDispatchService.dispatch_cad_emergency_packet(incident_id, bus_id, e_type, lat, lng, notes)
        return jsonify({"success": True, **res}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
