"""
CityBus Enterprise Platform - Trips API
File: backend/routes/trips.py
"""

from flask import Blueprint, request, jsonify
from services.trip_service import TripService
from repositories.trip_repository import TripRepository

trips_bp = Blueprint('trips_v1', __name__, url_prefix='/api/v1/trips')


@trips_bp.route('', methods=['GET'])
def get_trips():
    """Lists trips with status and driver filtering."""
    try:
        status = request.args.get('status')
        driver_id = request.args.get('driver_id')
        trips = TripRepository.get_all(status, int(driver_id) if driver_id else None)
        return jsonify({
            "success": True,
            "count": len(trips),
            "trips": [t.to_dict() for t in trips]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@trips_bp.route('/start', methods=['POST'])
def start_trip():
    """Starts a driver trip lifecycle."""
    try:
        data = request.get_json() or {}
        bus_id = data.get('bus_id')
        driver_id = data.get('driver_id')
        route_id = data.get('route_id')
        conductor_id = data.get('conductor_id')

        if not bus_id or not driver_id or not route_id:
            return jsonify({"success": False, "message": "Missing bus_id, driver_id, or route_id"}), 400

        trip = TripService.start_trip(bus_id, driver_id, route_id, conductor_id)
        return jsonify({
            "success": True,
            "message": "Trip started successfully",
            "trip": trip.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@trips_bp.route('/stop', methods=['POST'])
def stop_trip():
    """Ends an active trip."""
    try:
        data = request.get_json() or {}
        trip_id = data.get('trip_id')
        bus_id = data.get('bus_id')

        trip = TripService.stop_trip(trip_id, bus_id)
        if not trip:
            return jsonify({"success": False, "message": "Active trip not found"}), 404

        return jsonify({
            "success": True,
            "message": "Trip completed",
            "trip": trip.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
