"""
CityBus Enterprise Platform - Routes API
File: backend/routes/routes.py
"""

from flask import Blueprint, request, jsonify
from repositories.route_repository import RouteRepository

routes_bp = Blueprint('routes_v1', __name__, url_prefix='/api/v1/routes')


@routes_bp.route('', methods=['GET'])
def get_all_routes():
    """Lists all transit routes."""
    try:
        category = request.args.get('category')
        routes = RouteRepository.get_all(category)
        return jsonify({
            "success": True,
            "count": len(routes),
            "routes": [r.to_dict(include_stops=False) for r in routes]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@routes_bp.route('/<int:route_id>', methods=['GET'])
def get_single_route(route_id):
    """Returns single route details with complete ordered stops and waypoint geometry."""
    try:
        route = RouteRepository.get_by_id(route_id)
        if not route:
            return jsonify({"success": False, "message": f"Route {route_id} not found"}), 404

        return jsonify({
            "success": True,
            "route": route.to_dict(include_stops=True)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
