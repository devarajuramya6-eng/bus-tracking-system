"""
CityBus - Database Models (models.py)

Defines SQLite/SQLAlchemy tables for Bus, Route, Stop, Driver, Trip, and User.
Includes clean serialization helper methods (to_dict) for API responses.
"""

from datetime import datetime
from database import db


class Route(db.Model):
    """Transit route with origin, destination, and stop sequence."""
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    route_number = db.Column(db.String(20), nullable=False)
    start_point = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    estimated_time = db.Column(db.Integer, nullable=False)  # in minutes
    status = db.Column(db.String(50), default="Active")     # Active, Inactive

    # Relationships
    stops = db.relationship('Stop', backref='route', lazy=True, order_by='Stop.stop_order', cascade="all, delete-orphan")
    buses = db.relationship('Bus', backref='route_rel', lazy=True)

    def to_dict(self, include_stops=False):
        data = {
            "id": self.id,
            "route_number": self.route_number,
            "start_point": self.start_point,
            "destination": self.destination,
            "estimated_time": self.estimated_time,
            "status": self.status,
            "stops_count": len(self.stops)
        }
        if include_stops:
            data["stops"] = [stop.to_dict() for stop in self.stops]
        return data


class Driver(db.Model):
    """Registered fleet driver profile."""
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default="Active")  # Active, Break, Offline

    # Relationships
    buses = db.relationship('Bus', backref='driver_rel', lazy=True)
    trips = db.relationship('Trip', backref='driver_rel', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "status": self.status
        }


class Stop(db.Model):
    """Bus stop location assigned to a specific route."""
    __tablename__ = 'stops'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    stop_order = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "route_id": self.route_id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "stop_order": self.stop_order
        }


class Bus(db.Model):
    """Operating municipal bus with live GPS coordinates and telemetry."""
    __tablename__ = 'buses'

    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(20), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    speed = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default="On Route")  # On Route, Delayed, Offline
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trips = db.relationship('Trip', backref='bus_rel', lazy=True)

    def to_dict(self):
        route_title = "Unassigned"
        if self.route_rel:
            route_title = f"{self.route_rel.start_point} → {self.route_rel.destination}"

        driver_name = "Unassigned"
        if self.driver_rel:
            driver_name = self.driver_rel.name

        formatted_time = self.last_updated.strftime("%Y-%m-%d %H:%M:%S") if self.last_updated else datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "id": self.id,
            "bus_number": self.bus_number,
            "route_id": self.route_id,
            "route": route_title,
            "driver_id": self.driver_id,
            "driver": driver_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "speed": round(self.speed, 1),
            "status": self.status,
            "last_updated": formatted_time
        }


class Trip(db.Model):
    """Driver trip record lifecycle (Active -> Completed)."""
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default="Active")  # Active, Completed

    def to_dict(self):
        return {
            "id": self.id,
            "bus_id": self.bus_id,
            "driver_id": self.driver_id,
            "route_id": self.route_id,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else None,
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else None,
            "status": self.status
        }


class User(db.Model):
    """User profile for demo authentication (passenger, driver, admin)."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default="passenger")  # passenger, driver, admin

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }
