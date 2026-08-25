"""
CityBus Enterprise Platform - Transit Route, Stop, RouteStop & Schedule Models
File: backend/models/route.py
"""

from models.base import db, BaseModelMixin
import json


class Route(db.Model, BaseModelMixin):
    """Transit route entity with origin, destination, category, waypoints, and distance."""
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    route_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    start_point = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), default="Local", nullable=False) # Express, Local, Metro, Airport, Night
    estimated_time = db.Column(db.Integer, default=30, nullable=False)   # in minutes
    distance_km = db.Column(db.Float, default=15.0, nullable=False)
    base_fare = db.Column(db.Float, default=15.0, nullable=False)
    color_hex = db.Column(db.String(20), default="#2563EB", nullable=False)
    waypoints_json = db.Column(db.Text, nullable=True) # JSON Array of [lat, lng]
    status = db.Column(db.String(50), default="Active", nullable=False)

    # Relationships
    route_stops = db.relationship('RouteStop', backref='route_rel', lazy=True, order_by='RouteStop.stop_order', cascade="all, delete-orphan")
    buses = db.relationship('Bus', backref='route_rel', lazy=True)
    trips = db.relationship('Trip', backref='route_rel', lazy=True)
    schedules = db.relationship('Schedule', backref='route_rel', lazy=True, cascade="all, delete-orphan")

    def get_waypoints(self):
        try:
            return json.loads(self.waypoints_json) if self.waypoints_json else []
        except:
            return []

    def set_waypoints(self, points):
        self.waypoints_json = json.dumps(points)

    def to_dict(self, include_stops=False):
        data = super().to_dict()
        data['waypoints'] = self.get_waypoints()
        data['stops_count'] = len(self.route_stops)
        if include_stops:
            data['stops'] = [rs.to_dict() for rs in self.route_stops]
        return data


class Stop(db.Model, BaseModelMixin):
    """City transit stop location with geographic coordinates, amenities, and code."""
    __tablename__ = 'stops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    has_shelter = db.Column(db.Boolean, default=True, nullable=False)
    is_wheelchair_accessible = db.Column(db.Boolean, default=True, nullable=False)
    is_popular = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    route_stops = db.relationship('RouteStop', backref='stop_rel', lazy=True, cascade="all, delete-orphan")


class RouteStop(db.Model, BaseModelMixin):
    """Associates a Stop with a Route in a specific sequential order."""
    __tablename__ = 'route_stops'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False, index=True)
    stop_id = db.Column(db.Integer, db.ForeignKey('stops.id'), nullable=False, index=True)
    stop_order = db.Column(db.Integer, nullable=False)
    distance_from_origin_km = db.Column(db.Float, default=0.0, nullable=False)
    typical_dwell_seconds = db.Column(db.Integer, default=45, nullable=False)

    def to_dict(self):
        data = super().to_dict()
        if self.stop_rel:
            data['name'] = self.stop_rel.name
            data['code'] = self.stop_rel.code
            data['latitude'] = self.stop_rel.latitude
            data['longitude'] = self.stop_rel.longitude
        return data


class Schedule(db.Model, BaseModelMixin):
    """Timetable master schedules defining departure and frequency."""
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    departure_time = db.Column(db.String(10), nullable=False) # e.g. "06:30"
    frequency_minutes = db.Column(db.Integer, default=15, nullable=False)
    service_type = db.Column(db.String(30), default="Weekday", nullable=False) # Weekday, Weekend, Holiday, Special
    is_active = db.Column(db.Boolean, default=True, nullable=False)
