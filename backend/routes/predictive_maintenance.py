"""
CityBus Enterprise Platform - Predictive Maintenance API
File: backend/routes/predictive_maintenance.py

Provides ML failure probability scores, subsystem wear diagnostics, and maintenance schedules.
"""

from flask import Blueprint, jsonify
from services.predictive_mechanical_failure_model import PredictiveMechanicalFailureModel

predictive_maint_bp = Blueprint('predictive_maint_v1', __name__, url_prefix='/api/v1/predictive-maintenance')


@predictive_maint_bp.route('/bus/<int:bus_id>', methods=['GET'])
def get_bus_health(bus_id):
    """Returns predictive failure analysis for a bus."""
    try:
        data = PredictiveMechanicalFailureModel.evaluate_vehicle_health(bus_id)
        return jsonify({"success": True, **data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
