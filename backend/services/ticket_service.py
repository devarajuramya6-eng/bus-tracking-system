"""
CityBus Enterprise Platform - Ticketing & QR Service
File: backend/services/ticket_service.py
"""

from datetime import datetime, timedelta
import hmac
import hashlib
import json
import base64
from config import Config
from models import db, Ticket
from repositories.ticket_repository import TicketRepository
from repositories.user_repository import UserRepository


class TicketService:
    """Manages ticket issuance, fare calculation, cryptographic QR signatures, and validation."""

    @staticmethod
    def calculate_fare(distance_km, passenger_count=1, concession_type="general"):
        base = Config.BASE_FARE_INR
        rate = Config.RATE_PER_KM_INR
        raw_fare = base + (distance_km * rate)

        # Concessions
        discount = 0.0
        if concession_type == 'student':
            discount = 0.50
        elif concession_type == 'senior':
            discount = 0.30

        unit_fare = max(10.0, round(raw_fare * (1.0 - discount)))
        total_fare = unit_fare * passenger_count
        return {
            "unit_fare": unit_fare,
            "total_fare": total_fare,
            "passenger_count": passenger_count,
            "concession": concession_type
        }

    @staticmethod
    def generate_signed_qr_payload(ticket_number, user_id, amount):
        """Creates an HMAC-SHA256 cryptographically signed QR code payload."""
        data_str = f"CITYBUS|{ticket_number}|{user_id}|{amount}"
        signature = hmac.new(Config.SECRET_KEY.encode('utf-8'), data_str.encode('utf-8'), hashlib.sha256).hexdigest()[:16]
        payload = {
            "tck": ticket_number,
            "uid": user_id,
            "amt": amount,
            "sig": signature
        }
        return base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')

    @staticmethod
    def verify_qr_signature(payload_b64):
        try:
            raw = base64.b64decode(payload_b64.encode('utf-8')).decode('utf-8')
            data = json.loads(raw)
            ticket_number = data.get("tck")
            user_id = data.get("uid")
            amount = data.get("amt")
            expected_data_str = f"CITYBUS|{ticket_number}|{user_id}|{amount}"
            expected_sig = hmac.new(Config.SECRET_KEY.encode('utf-8'), expected_data_str.encode('utf-8'), hashlib.sha256).hexdigest()[:16]
            
            if data.get("sig") != expected_sig:
                return None, "INVALID_SIGNATURE"

            return data, None
        except:
            return None, "CORRUPT_PAYLOAD"

    @staticmethod
    def issue_ticket(user_id, route_id, origin, destination, fare_amount, passenger_count=1, bus_id=None):
        ticket_number = Ticket.generate_ticket_number()
        qr_payload = TicketService.generate_signed_qr_payload(ticket_number, user_id, fare_amount)
        
        ticket = Ticket(
            ticket_number=ticket_number,
            user_id=user_id,
            route_id=route_id,
            origin_stop=origin,
            destination_stop=destination,
            passenger_count=passenger_count,
            fare_amount=fare_amount,
            status="VALID",
            qr_payload=qr_payload,
            issued_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=6)
        )
        db.session.add(ticket)
        db.session.commit()

        UserRepository.log_audit("TICKET_ISSUED", "Ticket", ticket.id, f"Ticket {ticket.ticket_number} issued for Rs {fare_amount}", user_id)
        return ticket

    @staticmethod
    def validate_qr(qr_string, conductor_id=None):
        # Decode and verify signature
        data, err = TicketService.verify_qr_signature(qr_string)
        ticket_number = None

        if data:
            ticket_number = data.get("tck")
        else:
            # Fallback to plain ticket number if scanned directly
            ticket_number = qr_string.strip()

        ticket = TicketRepository.get_by_number(ticket_number)
        if not ticket:
            return None, "NOT_FOUND", "Ticket does not exist in system"

        validated_ticket, status = TicketRepository.validate_ticket(ticket.id, conductor_id)
        
        UserRepository.log_audit("TICKET_SCANNED", "Ticket", ticket.id, f"Ticket {ticket.ticket_number} validated: {status}", conductor_id)
        return validated_ticket, status, f"Validation status: {status}"
