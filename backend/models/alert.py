"""
CityBus Enterprise Platform - Alerts, Notifications, Favorites & Audit Models
File: backend/models/alert.py
"""

from datetime import datetime
from models.base import db, BaseModelMixin


class Alert(db.Model, BaseModelMixin):
    """Public passenger transit service alert and disruption warning."""
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(30), default="Warning", nullable=False) # Info, Warning, Critical
    
    target_scope = db.Column(db.String(40), default="All", nullable=False) # All, Route, Stop, Area
    target_route_id = db.Column(db.Integer, nullable=True)
    target_stop_id = db.Column(db.Integer, nullable=True)
    
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_by = db.Column(db.String(100), default="Dispatcher Control", nullable=False)


class Notification(db.Model, BaseModelMixin):
    """Targeted in-app passenger notification."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category = db.Column(db.String(40), default="System", nullable=False) # Bus, Ticket, Payment, Alert, Incident, Trip
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(30), default="info", nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    meta_json = db.Column(db.Text, nullable=True)


class Favorite(db.Model, BaseModelMixin):
    """Passenger saved favorites (bus, route, stop)."""
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    favorite_type = db.Column(db.String(30), nullable=False) # bus, route, stop
    target_id = db.Column(db.String(50), nullable=False)


class AuditLog(db.Model, BaseModelMixin):
    """Security and compliance administrative audit trail."""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    user_email = db.Column(db.String(120), nullable=True)
    action = db.Column(db.String(100), nullable=False, index=True)
    entity_type = db.Column(db.String(50), nullable=False)
    entity_id = db.Column(db.String(50), nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
