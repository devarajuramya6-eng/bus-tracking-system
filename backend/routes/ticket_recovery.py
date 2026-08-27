"""
CityBus Enterprise Platform - Ticket Recovery API
File: backend/routes/ticket_recovery.py

Provides self-service digital ticket recovery by transaction ID or phone.
"""

from flask import Blueprint, request, jsonify
from services.lost_ticket_recovery_service import LostTicketRecoveryService

ticket_recovery_bp = Blueprint('ticket_recovery_v1', __name__, url_prefix='/api/v1/ticket-recovery')


@ticket_recovery_bp.route('/lookup', methods=['POST'])
def lookup_ticket():
    """Recovers lost QR ticket by transaction reference."""
    try:
        data = request.get_json() or {}
        txn_id = data.get('transaction_id')
        phone = data.get('phone', '9848012345')

        if not txn_id:
            return jsonify({"success": False, "message": "transaction_id is required"}), 400

        ticket = LostTicketRecoveryService.recover_ticket_by_transaction(txn_id, phone)
        if not ticket:
            return jsonify({"success": False, "message": "No matching active ticket found"}), 404

        return jsonify({"success": True, "ticket": ticket}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
