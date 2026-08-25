"""
CityBus Enterprise Platform - Buses API Routes
File: backend/routes/buses.py
"""

from flask import Blueprint, request, jsonify
from repositories.bus_repository import BusRepository
from services.gps_service import GPSService
from services.eta_service import ETAService

buses_bp = Blueprint('buses_v1', __name__, url_prefix='/api/v1/buses')


@buses_bp.route('', methods=['GET'])
def get_all_buses():
    """Lists all operating buses with status filtering."""
    try:
        status_filter = request.args.get('status')
        route_filter = request.args.get('route_id')
        buses = BusRepository.get_all(status_filter, route_filter)

        return jsonify({
            "success": True,
            "count": len(buses),
            "buses": [bus.to_dict() for bus in buses]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@buses_bp.route('/<int:bus_id>', methods=['GET'])
def get_single_bus(bus_id):
    """Returns single bus details with dynamic calculated ETA."""
    try:
        bus = BusRepository.get_by_id(bus_id)
        if not bus:
            return jsonify({"success": False, "message": f"Bus with ID {bus_id} not found"}), 404

        bus_dict = bus.to_dict()
        eta_info = ETAService.calculate_eta(bus_id)
        bus_dict['telemetry_eta'] = eta_info

        return jsonify({
            "success": True,
            "bus": bus_dict
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@buses_bp.route('/nearby', methods=['GET'])
def get_nearby_buses():
    """Calculates distances from user coordinates and returns nearby buses with ETAs."""
    try:
        lat_str = request.args.get('lat')
        lng_str = request.args.get('lng')

        if not lat_str or not lng_str:
            return jsonify({
                "success": False,
                "message": "Missing 'lat' and 'lng' query params. Example: /api/v1/buses/nearby?lat=16.5062&lng=80.6480"
            }), 400

        user_lat = float(lat_str)
        user_lng = float(lng_str)
        radius_km = float(request.args.get('radius_km', 15.0))

        nearby_buses = BusRepository.get_nearby(user_lat, user_lng, radius_km)
        return jsonify({
            "success": True,
            "count": len(nearby_buses),
            "buses": nearby_buses
        }), 200

    except ValueError:
        return jsonify({"success": False, "message": "lat and lng must be valid numbers"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@buses_bp.route('/location', methods=['POST'])
def update_bus_location():
    """Receives live GPS telemetry ping from driver device or GPS tracker."""
    try:
        data = request.get_json() or {}
        bus_id = data.get('bus_id')
        lat = data.get('latitude')
        lng = data.get('longitude')
        speed = data.get('speed', 0.0)
        heading = data.get('heading')
        accuracy = data.get('accuracy', 5.0)

        if bus_id is None or lat is None or lng is None:
            return jsonify({"success": False, "message": "Missing bus_id, latitude, or longitude"}), 400

        result, err = GPSService.process_telemetry_ping(bus_id, lat, lng, speed, heading, accuracy)
        if err:
            return jsonify({"success": False, "message": err}), 404

        return jsonify({
            "success": True,
            "message": "Telemetry updated",
            **result
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
