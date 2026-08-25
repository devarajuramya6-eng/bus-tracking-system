"""
CityBus Enterprise Platform - Incident & Emergency Response Models
File: backend/models/incident.py
"""

from datetime import datetime
from models.base import db, BaseModelMixin


class Incident(db.Model, BaseModelMixin):
    """Transit incident and emergency dispatch log."""
    __tablename__ = 'incidents'

    id = db.Column(db.Integer, primary_key=True)
    incident_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Types: Accident, Breakdown, Traffic, Medical, Security, GPS_Failure, Mechanical, Route_Deviation, SOS_Emergency
    incident_type = db.Column(db.String(50), nullable=False, index=True)
    
    # Severity: Low, Medium, High, Critical, Priority-1
    severity = db.Column(db.String(30), default="Medium", nullable=False, index=True)
    
    # Kanban Status: New, Acknowledged, Assigned, In Progress, Resolved, Closed
    status = db.Column(db.String(40), default="New", nullable=False, index=True)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=True)
    
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    location_name = db.Column(db.String(150), nullable=True)
    
    reported_by_user_id = db.Column(db.Integer, nullable=True)
    assigned_dispatcher = db.Column(db.String(100), nullable=True)
    resolution_notes = db.Column(db.Text, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def generate_incident_number(cls):
        return f"INC-{datetime.utcnow().strftime('%y%m%d')}-{datetime.utcnow().strftime('%H%M%S')}"
