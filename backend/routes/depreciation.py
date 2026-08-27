"""
CityBus Enterprise Platform - Asset Depreciation & TCO API
File: backend/routes/depreciation.py

Provides municipal asset book valuation and lifecycle schedules.
"""

from flask import Blueprint, request, jsonify
from services.fleet_lifecycle_depreciation import FleetLifecycleDepreciation

depreciation_bp = Blueprint('depreciation_v1', __name__, url_prefix='/api/v1/depreciation')


@depreciation_bp.route('/bus/<int:bus_id>', methods=['GET'])
def get_bus_depreciation(bus_id):
    """Returns current book value and accumulated depreciation for a bus."""
    try:
        age_years = request.args.get('age_years', 3.5, type=float)
        data = FleetLifecycleDepreciation.calculate_vehicle_book_value(bus_id, age_years)
        return jsonify({"success": True, **data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
