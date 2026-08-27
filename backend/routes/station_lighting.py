"""
CityBus Enterprise Platform - Station Shelter Lighting API
File: backend/routes/station_lighting.py

Provides solar bus shelter IoT lighting telemetry and vandalism sensors.
"""

from flask import Blueprint, jsonify
from services.station_shelter_lighting_iot_service import StationShelterLightingIoTService

station_lighting_bp = Blueprint('station_lighting_v1', __name__, url_prefix='/api/v1/station-lighting')


@station_lighting_bp.route('/shelter/<int:stop_id>', methods=['GET'])
def get_shelter_iot(stop_id):
    """Returns solar battery and LED lighting telemetry."""
    try:
        data = StationShelterLightingIoTService.get_shelter_iot_telemetry(stop_id)
        return jsonify({"success": True, "shelter_telemetry": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
