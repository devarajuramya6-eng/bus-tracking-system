"""
CityBus Enterprise Platform - Route Timetable API
File: backend/routes/timetable.py

Provides public timetable matrices, frequency schedules, and stop arrival times.
"""

from flask import Blueprint, request, jsonify
from services.route_timetable_generator import RouteTimetableGenerator

timetable_bp = Blueprint('timetable_v1', __name__, url_prefix='/api/v1/timetable')


@timetable_bp.route('/route/<int:route_id>', methods=['GET'])
def get_route_timetable(route_id):
    """Returns static stop departure schedule for a route."""
    try:
        service_day = request.args.get('day', 'WEEKDAY')
        data = RouteTimetableGenerator.generate_route_timetable(route_id, service_day)
        return jsonify({"success": True, **data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
