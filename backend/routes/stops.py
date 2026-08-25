"""
CityBus Enterprise Platform - Stops API
File: backend/routes/stops.py
"""

from flask import Blueprint, request, jsonify
from repositories.route_repository import RouteRepository

stops_bp = Blueprint('stops_v1', __name__, url_prefix='/api/v1/stops')


@stops_bp.route('', methods=['GET'])
def get_all_stops():
    """Lists bus stops with optional route filtering."""
    try:
        route_id = request.args.get('route_id')
        stops = RouteRepository.get_all_stops(int(route_id) if route_id else None)

        return jsonify({
            "success": True,
            "count": len(stops),
            "stops": [s.to_dict() for s in stops]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@stops_bp.route('/<int:stop_id>', methods=['GET'])
def get_single_stop(stop_id):
    """Returns single stop details with next departures."""
    try:
        stop = RouteRepository.get_stop_by_id(stop_id)
        if not stop:
            return jsonify({"success": False, "message": f"Stop {stop_id} not found"}), 404

        return jsonify({
            "success": True,
            "stop": stop.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
