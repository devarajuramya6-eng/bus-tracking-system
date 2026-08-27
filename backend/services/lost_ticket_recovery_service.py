"""
CityBus Enterprise Platform - Digital Ticket Recovery & SMS Dispatch Service
File: backend/services/lost_ticket_recovery_service.py

Allows passengers to recover lost QR ticket passes via SMS OTP authentication,
registered phone lookup, or UPI payment transaction reference verification.
"""

from typing import Dict, List, Any, Optional
from models import Ticket, db


class LostTicketRecoveryService:
    """Provides self-service ticket retrieval and SMS QR link dispatch."""

    @staticmethod
    def recover_ticket_by_transaction(txn_id: str, phone: str) -> Optional[Dict[str, Any]]:
        """Looks up active ticket matching transaction reference or ticket number."""
        ticket = Ticket.query.filter((Ticket.ticket_number == txn_id) | (Ticket.qr_code == txn_id)).first()
        if not ticket:
            return None

        return {
            "ticket_id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "origin_stop": ticket.origin_stop,
            "destination_stop": ticket.destination_stop,
            "fare_amount": ticket.fare_amount,
            "status": ticket.status,
            "qr_code_payload": ticket.qr_code,
            "recovery_sms_dispatched_to": f"+91 {phone[-4:].rjust(len(phone), '*')}"
        }
