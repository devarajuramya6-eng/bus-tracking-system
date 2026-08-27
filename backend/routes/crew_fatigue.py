"""
CityBus Enterprise Platform - Crew Fatigue API
File: backend/routes/crew_fatigue.py

Provides DMS camera ingestion and driver fatigue alerts for dispatchers.
"""

from flask import Blueprint, request, jsonify
from services.crew_fatigue_monitor_service import CrewFatigueMonitorService

crew_fatigue_bp = Blueprint('crew_fatigue_v1', __name__, url_prefix='/api/v1/crew-fatigue')


@crew_fatigue_bp.route('/alerts', methods=['GET'])
def get_fatigue_alerts():
    """Returns active DMS fatigue alerts."""
    try:
        alerts = CrewFatigueMonitorService.get_recent_fatigue_alerts()
        return jsonify({"success": True, "count": len(alerts), "alerts": alerts}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@crew_fatigue_bp.route('/telemetry', methods=['POST'])
def ingest_dms_packet():
    """Ingests real-time driver DMS eye-tracking telemetry."""
    try:
        data = request.get_json() or {}
        driver_id = data.get('driver_id', 1)
        bus_id = data.get('bus_id', 1)
        perclos = float(data.get('perclos_ratio', 0.15))
        yawns = int(data.get('yawn_count', 0))
        pitch = float(data.get('head_pitch', 0.0))

        res = CrewFatigueMonitorService.process_dms_telemetry(driver_id, bus_id, perclos, yawns, pitch)
        return jsonify({"success": True, "dms_log": res}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
