"""
CityBus Enterprise Platform - Simulation Control API
File: backend/routes/simulation.py
"""

from flask import Blueprint, jsonify, request
from services.simulator_service import simulator_engine

simulation_bp = Blueprint('simulation_v1', __name__, url_prefix='/api/v1/simulation')


@simulation_bp.route('/step', methods=['POST'])
def step_simulation():
    """Manually triggers one kinematic progression step for all active buses."""
    try:
        updated_buses = simulator_engine.step_simulation()
        return jsonify({
            "success": True,
            "count": len(updated_buses),
            "buses": updated_buses
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@simulation_bp.route('/status', methods=['GET'])
def get_simulation_status():
    """Returns simulation engine state."""
    return jsonify({
        "success": True,
        "is_running": simulator_engine.is_running,
        "step_ratio": simulator_engine.step_ratio
    }), 200
