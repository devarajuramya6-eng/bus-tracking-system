"""
CityBus Enterprise Platform - Driver & Conductor Models
File: backend/models/driver.py, backend/models/conductor.py
"""

from models.base import db, BaseModelMixin


class Driver(db.Model, BaseModelMixin):
    """Registered municipal fleet driver profile."""
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    license_number = db.Column(db.String(60), nullable=False, unique=True)
    license_expiry = db.Column(db.DateTime, nullable=True)
    experience_years = db.Column(db.Integer, default=5, nullable=False)
    rating = db.Column(db.Float, default=4.8, nullable=False)
    status = db.Column(db.String(50), default="Active", nullable=False) # Active, On Break, Offline, Suspended

    # Relationships
    buses = db.relationship('Bus', backref='driver_rel', lazy=True)
    trips = db.relationship('Trip', backref='driver_rel', lazy=True)
    incidents = db.relationship('Incident', backref='driver_rel', lazy=True)


class Conductor(db.Model, BaseModelMixin):
    """Registered transit fare conductor profile."""
    __tablename__ = 'conductors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    badge_id = db.Column(db.String(60), nullable=False, unique=True)
    status = db.Column(db.String(50), default="Active", nullable=False)

    # Relationships
    buses = db.relationship('Bus', backref='conductor_rel', lazy=True)
    trips = db.relationship('Trip', backref='conductor_rel', lazy=True)
