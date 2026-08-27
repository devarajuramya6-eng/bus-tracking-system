"""
CityBus Enterprise Platform - AFC & Smart Card API
File: backend/routes/afc.py

Provides contactless card validation, purse top-up, and transaction queries.
"""

from flask import Blueprint, request, jsonify
from services.smart_card_afc_service import SmartCardAFCService

afc_bp = Blueprint('afc_v1', __name__, url_prefix='/api/v1/afc')


@afc_bp.route('/card/<card_uid>', methods=['GET'])
def get_card(card_uid):
    """Retrieves card balance and type."""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        card = SmartCardAFCService.get_or_register_card(card_uid, user_id)
        return jsonify({
            "success": True,
            "card_uid": card.card_uid,
            "balance": card.balance,
            "card_type": card.card_type,
            "status": card.status
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@afc_bp.route('/tap-in', methods=['POST'])
def tap_in():
    """Validates boarding tap-in."""
    try:
        data = request.get_json() or {}
        card_uid = data.get('card_uid')
        bus_id = data.get('bus_id', 1)
        stop_name = data.get('stop_name', 'Pandit Nehru Bus Station')

        if not card_uid:
            return jsonify({"success": False, "message": "card_uid is required"}), 400

        res = SmartCardAFCService.process_tap_in(card_uid, bus_id, stop_name)
        status_code = 200 if res.get('success') else 400
        return jsonify(res), status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@afc_bp.route('/tap-out', methods=['POST'])
def tap_out():
    """Validates alighting tap-out and deducts distance-based fare."""
    try:
        data = request.get_json() or {}
        card_uid = data.get('card_uid')
        bus_id = data.get('bus_id', 1)
        stop_name = data.get('stop_name', 'Benz Circle Junction')
        distance_km = float(data.get('distance_km', 8.5))

        if not card_uid:
            return jsonify({"success": False, "message": "card_uid is required"}), 400

        res = SmartCardAFCService.process_tap_out(card_uid, bus_id, stop_name, distance_km)
        status_code = 200 if res.get('success') else 400
        return jsonify(res), status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@afc_bp.route('/top-up', methods=['POST'])
def top_up():
    """Adds funds to the smart card stored value purse."""
    try:
        data = request.get_json() or {}
        card_uid = data.get('card_uid')
        amount = float(data.get('amount', 100.0))
        ref = data.get('payment_reference', 'UPI-REF-2608')

        if not card_uid or amount <= 0:
            return jsonify({"success": False, "message": "Valid card_uid and positive amount required"}), 400

        res = SmartCardAFCService.top_up_balance(card_uid, amount, ref)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
