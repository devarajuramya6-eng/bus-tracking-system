"""
CityBus Enterprise Platform - Ticket Vending Kiosk API
File: backend/routes/kiosk.py

Provides self-service ticket vending machine (TVM) transactions.
"""

from flask import Blueprint, request, jsonify
from services.transit_kiosk_pos_service import TransitKioskPOSService

kiosk_bp = Blueprint('kiosk_v1', __name__, url_prefix='/api/v1/kiosk')


@kiosk_bp.route('/status/<kiosk_id>', methods=['GET'])
def get_kiosk_status(kiosk_id):
    """Returns kiosk paper and cash box telemetry."""
    try:
        data = TransitKioskPOSService.get_kiosk_status(kiosk_id)
        if not data:
            return jsonify({"success": False, "message": "Kiosk not found"}), 404
        return jsonify({"success": True, "kiosk": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@kiosk_bp.route('/dispense', methods=['POST'])
def dispense_ticket():
    """Processes ticket purchase at self-service kiosk."""
    try:
        data = request.get_json() or {}
        kiosk_id = data.get('kiosk_id', 'TVM-PNBS-01')
        route_id = int(data.get('route_id', 1))
        origin = data.get('origin_stop', 'Pandit Nehru Bus Station')
        dest = data.get('dest_stop', 'Benz Circle')
        fare = float(data.get('fare_amount', 25.0))
        pay_method = data.get('payment_method', 'UPI')

        res = TransitKioskPOSService.issue_kiosk_ticket(kiosk_id, route_id, origin, dest, fare, pay_method)
        return jsonify({"success": True, "ticket": res}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
