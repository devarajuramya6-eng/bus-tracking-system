"""
CityBus Enterprise Platform - DRTS Microtransit API
File: backend/routes/drts.py

Provides on-demand booking endpoints for dynamic demand-responsive transit.
"""

from flask import Blueprint, request, jsonify
from services.demand_responsive_transit_service import DemandResponsiveTransitService

drts_bp = Blueprint('drts_v1', __name__, url_prefix='/api/v1/drts')


@drts_bp.route('/book', methods=['POST'])
def book_ride():
    """Books an on-demand microtransit feeder ride."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 1)
        origin_lat = float(data.get('origin_lat', 16.5062))
        origin_lng = float(data.get('origin_lng', 80.6480))
        dest_lat = float(data.get('dest_lat', 16.5186))
        dest_lng = float(data.get('dest_lng', 80.6200))
        passenger_count = int(data.get('passenger_count', 1))

        res = DemandResponsiveTransitService.request_ride(user_id, origin_lat, origin_lng, dest_lat, dest_lng, passenger_count)
        return jsonify({"success": True, **res}), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@drts_bp.route('/booking/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Retrieves live status of a microtransit booking."""
    try:
        res = DemandResponsiveTransitService.get_booking_status(booking_id)
        if not res:
            return jsonify({"success": False, "message": "Booking not found"}), 404
        return jsonify({"success": True, **res}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@drts_bp.route('/booking/<booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    """Cancels a microtransit booking."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 1)
        success = DemandResponsiveTransitService.cancel_booking(booking_id, user_id)
        if not success:
            return jsonify({"success": False, "message": "Could not cancel booking"}), 400
        return jsonify({"success": True, "message": "Booking cancelled"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
