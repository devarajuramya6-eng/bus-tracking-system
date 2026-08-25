"""
CityBus Enterprise Platform - Service Alerts API
File: backend/routes/alerts.py
"""

from flask import Blueprint, request, jsonify
from repositories.incident_repository import IncidentRepository

alerts_bp = Blueprint('alerts_v1', __name__, url_prefix='/api/v1/alerts')


@alerts_bp.route('', methods=['GET'])
def get_alerts():
    """Returns active public service disruption alerts."""
    try:
        alerts = IncidentRepository.get_active_alerts()
        return jsonify({
            "success": True,
            "count": len(alerts),
            "alerts": [a.to_dict() for a in alerts]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@alerts_bp.route('', methods=['POST'])
def create_alert():
    """Broadcasts a new transit service alert."""
    try:
        data = request.get_json() or {}
        title = data.get('title')
        description = data.get('description', '')
        severity = data.get('severity', 'Warning')
        target_scope = data.get('target_scope', 'All')
        target_route_id = data.get('target_route_id')

        if not title:
            return jsonify({"success": False, "message": "Missing alert title"}), 400

        alert = IncidentRepository.create_alert(title, description, severity, target_scope, target_route_id)
        return jsonify({
            "success": True,
            "message": "Alert broadcasted",
            "alert": alert.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
