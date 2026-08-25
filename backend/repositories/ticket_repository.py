"""
CityBus Enterprise Platform - Ticket & Payment Repository
File: backend/repositories/ticket_repository.py
"""

from datetime import datetime, timedelta
from models import db, Ticket, Payment, Refund, FareRule


class TicketRepository:
    """Isolates all database queries for Tickets, Payments, and Refunds."""

    @staticmethod
    def get_by_id(ticket_id):
        return Ticket.query.get(ticket_id)

    @staticmethod
    def get_by_number(ticket_number):
        return Ticket.query.filter_by(ticket_number=ticket_number).first()

    @staticmethod
    def get_by_user(user_id, limit=50):
        return Ticket.query.filter_by(user_id=user_id).order_by(Ticket.issued_at.desc()).limit(limit).all()

    @staticmethod
    def create_ticket(user_id, route_id, origin_stop, destination_stop, fare_amount, passenger_count=1, bus_id=None, qr_payload=""):
        ticket_number = Ticket.generate_ticket_number()
        ticket = Ticket(
            ticket_number=ticket_number,
            user_id=user_id,
            route_id=route_id,
            bus_id=bus_id,
            origin_stop=origin_stop,
            destination_stop=destination_stop,
            passenger_count=passenger_count,
            fare_amount=fare_amount,
            status="VALID",
            qr_payload=qr_payload or f"CITYBUS:{ticket_number}:{user_id}:{fare_amount}",
            issued_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=6)
        )
        db.session.add(ticket)
        db.session.commit()
        return ticket

    @staticmethod
    def validate_ticket(ticket_id, conductor_id=None):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None, "NOT_FOUND"

        if ticket.status == "USED":
            return ticket, "ALREADY_USED"

        if ticket.status == "CANCELLED" or ticket.status == "REFUNDED":
            return ticket, "CANCELLED"

        if datetime.utcnow() > ticket.expires_at:
            ticket.status = "EXPIRED"
            db.session.commit()
            return ticket, "EXPIRED"

        # Mark Validated
        ticket.status = "USED"
        ticket.validated_at = datetime.utcnow()
        ticket.validated_by_conductor_id = conductor_id
        db.session.commit()
        return ticket, "VALID"

    @staticmethod
    def create_payment(ticket_id, order_id, amount, payment_id=None, signature=None, status="SUCCESS"):
        payment = Payment(
            ticket_id=ticket_id,
            order_id=order_id,
            payment_id=payment_id,
            signature=signature,
            amount=amount,
            currency="INR",
            status=status
        )
        db.session.add(payment)
        db.session.commit()
        return payment
