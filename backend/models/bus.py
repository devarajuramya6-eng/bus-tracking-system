"""
CityBus Enterprise Platform - Bus Model
File: backend/models/bus.py
"""

from datetime import datetime
from models.base import db, BaseModelMixin


class Bus(db.Model, BaseModelMixin):
    """Operating municipal bus asset with live GPS coordinates, telemetry, and assignments."""
    __tablename__ = 'buses'

    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    registration_plate = db.Column(db.String(40), nullable=True)
    model = db.Column(db.String(100), default="City Metro Express", nullable=False)
    capacity = db.Column(db.Integer, default=45, nullable=False)
    fuel_type = db.Column(db.String(30), default="Diesel", nullable=False) # Diesel, Electric, CNG
    gps_device_id = db.Column(db.String(60), nullable=True, index=True)
    
    # Active Route & Driver References
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=True, index=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True, index=True)
    conductor_id = db.Column(db.Integer, db.ForeignKey('conductors.id'), nullable=True)

    # Telemetry State
    latitude = db.Column(db.Float, default=16.5062, nullable=False)
    longitude = db.Column(db.Float, default=80.6480, nullable=False)
    speed = db.Column(db.Float, default=0.0, nullable=False)
    heading = db.Column(db.Float, default=0.0, nullable=False)
    accuracy = db.Column(db.Float, default=5.0, nullable=False)
    status = db.Column(db.String(50), default="On Route", nullable=False, index=True) # On Route, Delayed, Offline, Maintenance, Emergency
    occupancy = db.Column(db.Integer, default=0, nullable=False) # Current passenger count
    odometer_km = db.Column(db.Float, default=1000.0, nullable=False)
    
    last_gps_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    trips = db.relationship('Trip', backref='bus_rel', lazy=True)
    telemetry_logs = db.relationship('Telemetry', backref='bus_rel', lazy=True, cascade="all, delete-orphan")
    work_orders = db.relationship('MaintenanceWorkOrder', backref='bus_rel', lazy=True)
    fuel_logs = db.relationship('FuelLog', backref='bus_rel', lazy=True)

    def to_dict(self):
        data = super().to_dict()
        route_num = getattr(self.route_rel, 'route_number', '') if self.route_rel else ""
        data['route_number'] = route_num
        data['number'] = self.bus_number
        data['route'] = f"{self.route_rel.start_point} → {self.route_rel.destination}" if self.route_rel else "Unassigned"
        data['driver'] = self.driver_rel.name if self.driver_rel else "Unassigned"
        data['conductor'] = self.conductor_rel.name if self.conductor_rel else "Unassigned"
        data['speed'] = round(self.speed, 1)
        data['last_updated'] = self.last_gps_update.strftime("%Y-%m-%d %H:%M:%S") if self.last_gps_update else "Just now"
        return data
