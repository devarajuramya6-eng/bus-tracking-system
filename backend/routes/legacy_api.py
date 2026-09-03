"""
CityBus Enterprise Platform - Legacy API Compatibility Layer
File: backend/routes/legacy_api.py

Provides backward-compatible routes for `/api/buses`, `/api/routes`,
`/api/stops`, `/api/trips`, and `/api/login` without breaking legacy client integrations.
"""

from flask import Blueprint, request, jsonify
from repositories.bus_repository import BusRepository
from repositories.route_repository import RouteRepository
from repositories.trip_repository import TripRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.gps_service import GPSService
from models import Stop

legacy_bp = Blueprint('legacy_api', __name__, url_prefix='/api')


@legacy_bp.route('/buses', methods=['GET'])
def legacy_get_all_buses():
    """Returns all buses with optional search and status filtering."""
    try:
        status_filter = request.args.get('status')
        route_filter = request.args.get('route_id')
        search_query = request.args.get('q') or request.args.get('search')
        buses = BusRepository.get_all(status_filter, route_filter, search=search_query)
        return jsonify({
            "success": True,
            "count": len(buses),
            "buses": [bus.to_dict() for bus in buses]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@legacy_bp.route('/buses/<int:bus_id>', methods=['GET'])
def legacy_get_single_bus(bus_id):
    """Returns a single bus."""
    try:
        bus = BusRepository.get_by_id(bus_id)
        if not bus:
            return jsonify({"success": False, "message": f"Bus with ID {bus_id} not found"}), 404
        return jsonify({"success": True, "bus": bus.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@legacy_bp.route('/buses/nearby', methods=['GET'])
def legacy_get_nearby_buses():
    """Returns nearby buses for given lat/lng."""
    try:
        lat = float(request.args.get('lat', 16.5062))
        lng = float(request.args.get('lng', 80.6480))
        radius = float(request.args.get('radius_km', 15.0))
        nearby = BusRepository.get_nearby(lat, lng, radius)
        return jsonify({"success": True, "count": len(nearby), "buses": nearby}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@legacy_bp.route('/buses/location', methods=['POST'])
def legacy_update_location():
    """Updates GPS location for a bus."""
    try:
        data = request.get_json() or {}
        bus_id = data.get('bus_id')
        lat = data.get('latitude')
        lng = data.get('longitude')
        speed = data.get('speed', 0.0)
        heading = data.get('heading')
        
        if bus_id is None or lat is None or lng is None:
            return jsonify({"success": False, "message": "Missing required fields"}), 400
            
        result, err = GPSService.process_telemetry_ping(bus_id, lat, lng, speed, heading)
        if err:
            return jsonify({"success": False, "message": err}), 404
        return jsonify({"success": True, "bus_id": bus_id, **result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@legacy_bp.route('/routes', methods=['GET'])
def legacy_get_all_routes():
    """Returns all routes."""
    try:
        routes = RouteRepository.get_all()
        return jsonify({
            "success": True,
            "count": len(routes),
            "routes": [r.to_dict() for r in routes]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@legacy_bp.route('/routes/<int:route_id>', methods=['GET'])
def legacy_get_single_route(route_id):
    """Returns a single route with stops."""
    try:
        route = RouteRepository.get_by_id(route_id)
        if not route:
            return jsonify({"success": False, "message": "Route not found"}), 404
        return jsonify({"success": True, "route": route.to_dict(include_stops=True)}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@legacy_bp.route('/stops', methods=['GET'])
def legacy_get_all_stops():
    """Returns all stops."""
    try:
        stops = Stop.query.all()
        return jsonify({
            "success": True,
            "count": len(stops),
            "stops": [s.to_dict() for s in stops]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@legacy_bp.route('/trips/start', methods=['POST'])
def legacy_start_trip():
    """Starts a new trip."""
    try:
        data = request.get_json() or {}
        bus_id = data.get('bus_id')
        driver_id = data.get('driver_id')
        route_id = data.get('route_id')

        if not bus_id or not driver_id or not route_id:
            return jsonify({"success": False, "message": "bus_id, driver_id, and route_id are required"}), 400

        trip = TripRepository.start_trip(bus_id, driver_id, route_id)
        return jsonify({"success": True, "trip_id": trip.id, "trip": trip.to_dict()}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@legacy_bp.route('/trips/stop', methods=['POST'])
def legacy_stop_trip():
    """Stops an active trip."""
    try:
        data = request.get_json() or {}
        trip_id = data.get('trip_id')
        bus_id = data.get('bus_id')
        trip = TripRepository.stop_trip(trip_id=trip_id, bus_id=bus_id)
        if not trip:
            return jsonify({"success": False, "message": "Trip not found or already completed"}), 404
        return jsonify({"success": True, "trip": trip.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@legacy_bp.route('/login', methods=['POST'])
def legacy_login():
    """Authenticates user."""
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password required"}), 400

        user = UserRepository.get_by_email(email)
        if not user or not user.check_password(password):
            return jsonify({"success": False, "message": "Invalid email or password"}), 401

        tokens = AuthService.generate_tokens(user)
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": user.to_dict(),
            **tokens
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
