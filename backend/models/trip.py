"""
CityBus Enterprise Platform - Trip, TripStop & Telemetry Models
File: backend/models/trip.py, backend/models/telemetry.py
"""

from datetime import datetime
from models.base import db, BaseModelMixin


class Trip(db.Model, BaseModelMixin):
    """Driver trip execution instance."""
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False, index=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False, index=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False, index=True)
    conductor_id = db.Column(db.Integer, db.ForeignKey('conductors.id'), nullable=True)

    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default="Active", nullable=False, index=True) # Active, Paused, Completed, Cancelled
    
    current_stop_sequence = db.Column(db.Integer, default=1, nullable=False)
    passenger_boarded_count = db.Column(db.Integer, default=0, nullable=False)
    total_fare_collected = db.Column(db.Float, default=0.0, nullable=False)

    # Relationships
    trip_stops = db.relationship('TripStop', backref='trip_rel', lazy=True, cascade="all, delete-orphan")


class TripStop(db.Model, BaseModelMixin):
    """Logs actual arrival and departure timestamps at each stop for a trip."""
    __tablename__ = 'trip_stops'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False, index=True)
    stop_id = db.Column(db.Integer, db.ForeignKey('stops.id'), nullable=False)
    stop_sequence = db.Column(db.Integer, nullable=False)
    
    scheduled_arrival = db.Column(db.DateTime, nullable=True)
    actual_arrival = db.Column(db.DateTime, nullable=True)
    actual_departure = db.Column(db.DateTime, nullable=True)
    passengers_boarded = db.Column(db.Integer, default=0, nullable=False)
    passengers_alighted = db.Column(db.Integer, default=0, nullable=False)


class Telemetry(db.Model, BaseModelMixin):
    """Historical GPS telemetry coordinate ping."""
    __tablename__ = 'telemetries'

    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False, index=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=True)
    
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    speed_kmh = db.Column(db.Float, default=0.0, nullable=False)
    heading_deg = db.Column(db.Float, default=0.0, nullable=False)
    accuracy_m = db.Column(db.Float, default=5.0, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
