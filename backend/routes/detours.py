"""
CityBus Enterprise Platform - Route Detours API
File: backend/routes/detours.py

Simulates temporary bypasses and road construction reroutes.
"""

from flask import Blueprint, request, jsonify
from services.route_detour_simulator import RouteDetourSimulator

detours_bp = Blueprint('detours_v1', __name__, url_prefix='/api/v1/detours')


@detours_bp.route('/simulate', methods=['POST'])
def simulate_detour():
    """Calculates alternate corridor trajectory for blocked road."""
    try:
        data = request.get_json() or {}
        route_id = int(data.get('route_id', 1))
        blocked_stop = data.get('blocked_stop', 'Benz Circle Main Underpass')
        reason = data.get('reason', 'Flyover Maintenance')

        res = RouteDetourSimulator.simulate_detour(route_id, blocked_stop, reason)
        return jsonify({"success": True, **res}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
