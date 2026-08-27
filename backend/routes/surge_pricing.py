"""
CityBus Enterprise Platform - Surge Pricing API
File: backend/routes/surge_pricing.py

Calculates dynamic peak demand fares and festival pricing multipliers.
"""

from flask import Blueprint, request, jsonify
from services.dynamic_pricing_surge_service import DynamicPricingSurgeService

surge_bp = Blueprint('surge_v1', __name__, url_prefix='/api/v1/surge')


@surge_bp.route('/calculate', methods=['GET', 'POST'])
def calculate_surge():
    """Calculates modified fare with surge multipliers."""
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args

        base_fare = float(data.get('base_fare', 25.0))
        event_code = data.get('event_code')
        occupancy = float(data.get('occupancy_pct', 50.0))

        res = DynamicPricingSurgeService.calculate_surge_fare(base_fare, event_code, occupancy)
        return jsonify({"success": True, **res}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
