"""
CityBus Enterprise Platform - Telemetry & GPS Ingestion API
File: backend/routes/telemetry.py

Handles high-frequency GPS telemetry ingestion from vehicle OBD-II trackers
and driver smartphone devices with Kalman filtering and speed validation.
"""

from flask import Blueprint, request, jsonify
from repositories.telemetry_repository import TelemetryRepository
from repositories.bus_repository import BusRepository
from services.gps_service import GPSService
from models import Telemetry, Bus, db

telemetry_bp = Blueprint('telemetry_v1', __name__, url_prefix='/api/v1/telemetry')


@telemetry_bp.route('/ping', methods=['POST'])
def ingest_telemetry_ping():
    """Ingests a single GPS coordinate ping with Kalman noise smoothing."""
    try:
        data = request.get_json() or {}
        bus_id = data.get('bus_id')
        lat = data.get('latitude')
        lng = data.get('longitude')
        speed = float(data.get('speed', 0.0))
        heading = float(data.get('heading', 0.0)) if data.get('heading') is not None else None
        accuracy = float(data.get('accuracy', 5.0))
        altitude = float(data.get('altitude', 0.0))

        if bus_id is None or lat is None or lng is None:
            return jsonify({"success": False, "message": "bus_id, latitude, and longitude are required"}), 400

        # Validate coordinate boundaries (Vijayawada Andhra Pradesh Transit Region)
        if not (15.0 <= float(lat) <= 18.0 and 79.0 <= float(lng) <= 82.0):
            return jsonify({"success": False, "message": "GPS coordinates out of Vijayawada transit bounds"}), 422

        result, err = GPSService.process_telemetry_ping(bus_id, float(lat), float(lng), speed, heading, accuracy)
        if err:
            return jsonify({"success": False, "message": err}), 404

        # Record breadcrumb log
        TelemetryRepository.record_ping(bus_id, float(lat), float(lng), speed, heading, accuracy, result.get('trip_id'))

        return jsonify({
            "success": True,
            "message": "Telemetry accepted and smoothed",
            **result
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@telemetry_bp.route('/batch', methods=['POST'])
def ingest_batch_telemetry():
    """Ingests a batch array of buffered GPS telemetry pings (offline sync)."""
    try:
        data = request.get_json() or {}
        pings = data.get('pings', [])
        if not pings:
            return jsonify({"success": False, "message": "pings array is required"}), 400

        processed = 0
        for p in pings:
            bus_id = p.get('bus_id')
            lat = p.get('latitude')
            lng = p.get('longitude')
            speed = float(p.get('speed', 0.0))
            heading = float(p.get('heading', 0.0)) if p.get('heading') is not None else None
            accuracy = float(p.get('accuracy', 5.0))
            
            if bus_id and lat and lng:
                GPSService.process_telemetry_ping(bus_id, float(lat), float(lng), speed, heading, accuracy)
                TelemetryRepository.record_ping(bus_id, float(lat), float(lng), speed, heading, accuracy)
                processed += 1

        return jsonify({
            "success": True,
            "message": f"Processed {processed} buffered telemetry pings"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@telemetry_bp.route('/trail/<int:bus_id>', methods=['GET'])
def get_bus_trail(bus_id):
    """Retrieves the recent breadcrumb GPS trail for Leaflet map polylines."""
    try:
        limit = int(request.args.get('limit', 50))
        trail = TelemetryRepository.get_recent_trail(bus_id, limit)
        stats = TelemetryRepository.get_bus_telemetry_stats(bus_id)
        
        return jsonify({
            "success": True,
            "bus_id": bus_id,
            "count": len(trail),
            "trail": trail,
            "stats": stats
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@telemetry_bp.route('/trip/<int:trip_id>', methods=['GET'])
def get_trip_trail(trip_id):
    """Retrieves all GPS points recorded during an entire trip for trajectory replay."""
    try:
        trail = TelemetryRepository.get_trip_trail(trip_id)
        return jsonify({
            "success": True,
            "trip_id": trip_id,
            "count": len(trail),
            "trail": trail
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
