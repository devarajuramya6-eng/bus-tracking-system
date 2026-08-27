"""
CityBus Enterprise Platform - Cabin Air Quality API
File: backend/routes/air_quality.py

Provides in-cabin PM2.5, AQI, and CO2 environmental telemetry.
"""

from flask import Blueprint, jsonify
from services.bus_interior_air_quality_service import BusInteriorAirQualityService

air_quality_bp = Blueprint('air_quality_v1', __name__, url_prefix='/api/v1/air-quality')


@air_quality_bp.route('/bus/<int:bus_id>', methods=['GET'])
def get_bus_air_quality(bus_id):
    """Returns in-cabin air quality index and ionizer state."""
    try:
        data = BusInteriorAirQualityService.get_cabin_iaq_telemetry(bus_id)
        return jsonify({"success": True, "cabin_iaq": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
