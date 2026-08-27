"""
CityBus Enterprise Platform - Multimodal Journey Planning API
File: backend/routes/multimodal.py

Calculates multi-modal urban transit plans combining bus, walking, and microtransit.
"""

from flask import Blueprint, request, jsonify
from services.multimodal_journey_planner import MultimodalJourneyPlanner

multimodal_bp = Blueprint('multimodal_v1', __name__, url_prefix='/api/v1/multimodal')


@multimodal_bp.route('/plan', methods=['GET', 'POST'])
def plan_multimodal_trip():
    """Generates multimodal travel itineraries."""
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args

        orig_lat = float(data.get('origin_lat', 16.5062))
        orig_lng = float(data.get('origin_lng', 80.6480))
        dest_lat = float(data.get('dest_lat', 16.5186))
        dest_lng = float(data.get('dest_lng', 80.6200))
        pref = data.get('preference', 'fastest')

        itineraries = MultimodalJourneyPlanner.plan_multimodal_trip(orig_lat, orig_lng, dest_lat, dest_lng, pref)
        return jsonify({"success": True, "itineraries": itineraries}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
