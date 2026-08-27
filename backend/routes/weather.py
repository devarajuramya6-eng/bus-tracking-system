"""
CityBus Enterprise Platform - Weather Impact API
File: backend/routes/weather.py

Provides transit weather alerts, safe speed caps, and road advisories.
"""

from flask import Blueprint, request, jsonify
from services.weather_impact_advisory_service import WeatherImpactAdvisoryService

weather_bp = Blueprint('weather_v1', __name__, url_prefix='/api/v1/weather')


@weather_bp.route('/advisory', methods=['GET'])
def get_weather_advisory():
    """Returns weather condition safety recommendations."""
    try:
        cond = request.args.get('condition', 'CLEAR')
        data = WeatherImpactAdvisoryService.get_weather_transit_advisory(cond)
        return jsonify({"success": True, "weather_advisory": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
