"""
CityBus Enterprise Platform - Dynamic ETA Calculation API
File: backend/routes/eta.py

Provides real-time Estimated Time of Arrival (ETA) predictions incorporating
live bus telemetry, route shape polylines, stop dwell times, and traffic delays.
"""

from flask import Blueprint, request, jsonify
from services.eta_service import ETAService
from repositories.bus_repository import BusRepository
from repositories.route_repository import RouteRepository
from repositories.stop_repository import StopRepository

eta_bp = Blueprint('eta_v1', __name__, url_prefix='/api/v1/eta')


@eta_bp.route('/bus/<int:bus_id>', methods=['GET'])
def get_bus_eta(bus_id):
    """Calculates real-time ETA for a bus to all remaining stops along its route."""
    try:
        bus = BusRepository.get_by_id(bus_id)
        if not bus:
            return jsonify({"success": False, "message": "Bus not found"}), 404

        eta_data = ETAService.calculate_eta(bus_id)
        return jsonify({
            "success": True,
            "bus_id": bus_id,
            "bus_number": bus.bus_number,
            "status": bus.status,
            "speed_kmh": round(bus.speed, 1),
            "eta": eta_data
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@eta_bp.route('/stop/<int:stop_id>', methods=['GET'])
def get_stop_arrivals(stop_id):
    """Calculates upcoming bus arrival ETAs for all buses approaching a specific stop."""
    try:
        stop = StopRepository.get_by_id(stop_id)
        if not stop:
            return jsonify({"success": False, "message": "Stop not found"}), 404

        # Find all active buses and check their ETA to this stop
        all_buses = BusRepository.get_all(status="On Route")
        arrivals = []

        for bus in all_buses:
            if not bus.route_id:
                continue
            eta_info = ETAService.calculate_eta(bus.id)
            if eta_info and 'stops_eta' in eta_info:
                for s_eta in eta_info['stops_eta']:
                    if s_eta.get('stop_id') == stop_id:
                        arrivals.append({
                            "bus_id": bus.id,
                            "bus_number": bus.bus_number,
                            "route_number": bus.route_rel.route_number if bus.route_rel else "Express",
                            "destination": bus.route_rel.destination if bus.route_rel else "",
                            "eta_minutes": s_eta.get('eta_minutes', 5),
                            "distance_km": s_eta.get('distance_km', 2.0),
                            "crowding": bus.occupancy,
                            "bus_model": bus.model
                        })

        arrivals.sort(key=lambda a: a['eta_minutes'])

        return jsonify({
            "success": True,
            "stop_id": stop.id,
            "stop_name": stop.name,
            "stop_code": stop.stop_code,
            "upcoming_arrivals_count": len(arrivals),
            "arrivals": arrivals
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@eta_bp.route('/route/<int:route_id>', methods=['GET'])
def get_route_headway_eta(route_id):
    """Calculates headway frequency and bus spacing along an entire corridor."""
    try:
        route = RouteRepository.get_by_id(route_id)
        if not route:
            return jsonify({"success": False, "message": "Route not found"}), 404

        buses = BusRepository.get_all(route_id=route_id)
        bus_etas = []
        for bus in buses:
            eta_data = ETAService.calculate_eta(bus.id)
            bus_etas.append({
                "bus_id": bus.id,
                "bus_number": bus.bus_number,
                "status": bus.status,
                "current_lat": bus.latitude,
                "current_lng": bus.longitude,
                "eta_summary": eta_data
            })

        return jsonify({
            "success": True,
            "route_id": route.id,
            "route_number": route.route_number,
            "active_buses_count": len(buses),
            "buses": bus_etas
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
