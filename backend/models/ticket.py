"""
CityBus Enterprise Platform - Digital Ticket, Payment, Refund & Fare Models
File: backend/models/ticket.py
"""

from datetime import datetime, timedelta
import uuid
from models.base import db, BaseModelMixin


class Ticket(db.Model, BaseModelMixin):
    """Digital transit ticket with cryptographic QR payload and lifecycle state machine."""
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=True)

    origin_stop = db.Column(db.String(120), nullable=False)
    destination_stop = db.Column(db.String(120), nullable=False)
    passenger_count = db.Column(db.Integer, default=1, nullable=False)
    fare_amount = db.Column(db.Float, nullable=False)
    
    # State: VALID, USED, EXPIRED, CANCELLED, REFUNDED
    status = db.Column(db.String(40), default="VALID", nullable=False, index=True)
    qr_payload = db.Column(db.Text, nullable=False)
    
    issued_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    validated_at = db.Column(db.DateTime, nullable=True)
    validated_by_conductor_id = db.Column(db.Integer, nullable=True)

    # Relationships
    payment = db.relationship('Payment', backref='ticket_rel', uselist=False, lazy=True)
    refund = db.relationship('Refund', backref='ticket_rel', uselist=False, lazy=True)

    @classmethod
    def generate_ticket_number(cls):
        return f"TCK-{datetime.utcnow().strftime('%y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    def to_dict(self):
        data = super().to_dict()
        data['is_expired'] = datetime.utcnow() > self.expires_at if self.expires_at else False
        return data


class Payment(db.Model, BaseModelMixin):
    """Financial payment ledger record with Razorpay transaction IDs and signatures."""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False, unique=True)
    order_id = db.Column(db.String(80), unique=True, nullable=False, index=True) # e.g. order_Kj29xZ...
    payment_id = db.Column(db.String(80), nullable=True, index=True)            # e.g. pay_92kxZ...
    signature = db.Column(db.String(255), nullable=True)
    
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="INR", nullable=False)
    payment_method = db.Column(db.String(50), default="UPI", nullable=False) # UPI, Card, NetBanking, Wallet, Cash
    status = db.Column(db.String(40), default="SUCCESS", nullable=False)     # CREATED, SUCCESS, FAILED, REFUNDED


class Refund(db.Model, BaseModelMixin):
    """Refund workflow transaction."""
    __tablename__ = 'refunds'

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False, unique=True)
    refund_amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(40), default="PROCESSED", nullable=False) # PENDING, PROCESSED, REJECTED
    processed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class FareRule(db.Model, BaseModelMixin):
    """Fare computation matrix and concession discount definitions."""
    __tablename__ = 'fare_rules'

    id = db.Column(db.Integer, primary_key=True)
    rule_name = db.Column(db.String(100), nullable=False)
    rule_type = db.Column(db.String(50), default="distance_based", nullable=False) # flat, distance_based, route_specific
    base_fare = db.Column(db.Float, default=15.0, nullable=False)
    rate_per_km = db.Column(db.Float, default=1.50, nullable=False)
    student_discount_pct = db.Column(db.Float, default=50.0, nullable=False)
    senior_discount_pct = db.Column(db.Float, default=30.0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
