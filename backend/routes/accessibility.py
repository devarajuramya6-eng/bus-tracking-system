"""
CityBus Enterprise Platform - Accessibility & Special Needs API
File: backend/routes/accessibility.py

Provides wheelchair-accessible route queries and accessible vehicle amenities.
"""

from flask import Blueprint, jsonify
from services.accessibility_route_planner import AccessibilityRoutePlanner

accessibility_bp = Blueprint('accessibility_v1', __name__, url_prefix='/api/v1/accessibility')


@accessibility_bp.route('/routes', methods=['GET'])
def get_accessible_routes():
    """Returns routes with ramp-equipped low floor buses."""
    try:
        routes = AccessibilityRoutePlanner.get_accessible_routes()
        return jsonify({"success": True, "accessible_routes": routes}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
