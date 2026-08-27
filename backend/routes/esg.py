"""
CityBus Enterprise Platform - ESG Environmental Impact API
File: backend/routes/esg.py

Provides sustainability metrics, CO2 emissions avoidance, and tree equivalent counts.
"""

from flask import Blueprint, jsonify
from services.co2_emission_calculator import CO2EmissionCalculator

esg_bp = Blueprint('esg_v1', __name__, url_prefix='/api/v1/esg')


@esg_bp.route('/metrics', methods=['GET'])
def get_esg_metrics():
    """Returns aggregated environmental sustainability metrics."""
    try:
        data = CO2EmissionCalculator.calculate_fleet_esg_impact()
        return jsonify({"success": True, "esg_metrics": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
