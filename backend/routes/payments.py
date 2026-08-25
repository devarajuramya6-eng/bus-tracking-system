"""
CityBus Enterprise Platform - Payments API
File: backend/routes/payments.py
"""

from flask import Blueprint, request, jsonify
from services.payment_service import PaymentService

payments_bp = Blueprint('payments_v1', __name__, url_prefix='/api/v1/payments')


@payments_bp.route('/order', methods=['POST'])
def create_payment_order():
    """Generates a Razorpay sandbox order for ticket checkout."""
    try:
        data = request.get_json() or {}
        ticket_id = data.get('ticket_id')
        amount = float(data.get('amount', 30.0))

        if not ticket_id:
            return jsonify({"success": False, "message": "Missing ticket_id"}), 400

        order_data = PaymentService.create_order(ticket_id, amount)
        return jsonify({
            "success": True,
            **order_data
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@payments_bp.route('/verify', methods=['POST'])
def verify_payment():
    """Verifies Razorpay digital signature and completes payment ledger."""
    try:
        data = request.get_json() or {}
        order_id = data.get('order_id')
        payment_id = data.get('payment_id')
        signature = data.get('signature', 'demo_signature_valid')

        if not order_id or not payment_id:
            return jsonify({"success": False, "message": "Missing order_id or payment_id"}), 400

        success, msg = PaymentService.process_successful_payment(order_id, payment_id, signature)
        if not success:
            return jsonify({"success": False, "message": msg}), 400

        return jsonify({
            "success": True,
            "message": "Payment verified and recorded successfully"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
