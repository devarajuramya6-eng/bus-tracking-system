"""
CityBus Enterprise Platform - Ticketing API
File: backend/routes/tickets.py
"""

from flask import Blueprint, request, jsonify
from services.ticket_service import TicketService
from repositories.ticket_repository import TicketRepository

tickets_bp = Blueprint('tickets_v1', __name__, url_prefix='/api/v1/tickets')


@tickets_bp.route('', methods=['POST'])
def create_ticket():
    """Books and issues a new digital pass with cryptographic QR code."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 1)
        route_id = data.get('route_id', 1)
        origin = data.get('origin', 'Vijayawada PNBS')
        destination = data.get('destination', 'Guntur')
        fare_amount = float(data.get('fare_amount', 30.0))
        passenger_count = int(data.get('passenger_count', 1))
        bus_id = data.get('bus_id')

        ticket = TicketService.issue_ticket(
            user_id=user_id,
            route_id=route_id,
            origin=origin,
            destination=destination,
            fare_amount=fare_amount,
            passenger_count=passenger_count,
            bus_id=bus_id
        )

        return jsonify({
            "success": True,
            "message": "Ticket created successfully",
            "ticket": ticket.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@tickets_bp.route('/validate', methods=['POST'])
def validate_ticket():
    """Validates scanned QR code string (called by conductor terminal)."""
    try:
        data = request.get_json() or {}
        qr_payload = data.get('qr_payload')
        conductor_id = data.get('conductor_id')

        if not qr_payload:
            return jsonify({"success": False, "message": "Missing qr_payload"}), 400

        ticket, status, message = TicketService.validate_qr(qr_payload, conductor_id)
        if not ticket:
            return jsonify({"success": False, "validation_status": status, "message": message}), 404

        return jsonify({
            "success": status == "VALID",
            "validation_status": status,
            "message": message,
            "ticket": ticket.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@tickets_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_tickets(user_id):
    """Returns digital passes for a passenger."""
    try:
        tickets = TicketRepository.get_by_user(user_id)
        return jsonify({
            "success": True,
            "count": len(tickets),
            "tickets": [t.to_dict() for t in tickets]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
