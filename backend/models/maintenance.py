"""
CityBus Enterprise Platform - Maintenance Work Orders & Fuel Logs
File: backend/models/maintenance.py, backend/models/fuel.py
"""

from datetime import datetime
from models.base import db, BaseModelMixin


class MaintenanceWorkOrder(db.Model, BaseModelMixin):
    """Vehicle maintenance work order and service interval."""
    __tablename__ = 'maintenance_work_orders'

    id = db.Column(db.Integer, primary_key=True)
    work_order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False, index=True)
    
    # Service Type: Scheduled, Oil_Change, Brake_Service, Engine_Overhaul, Tire_Replacement, Electrical, Inspection
    service_type = db.Column(db.String(60), nullable=False)
    
    # Status: Due, Overdue, In Progress, Completed, Critical
    status = db.Column(db.String(40), default="Due", nullable=False, index=True)
    priority = db.Column(db.String(30), default="Medium", nullable=False) # Low, Medium, High, Critical
    
    technician_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    parts_replaced = db.Column(db.String(255), nullable=True)
    
    cost_inr = db.Column(db.Float, default=0.0, nullable=False)
    downtime_hours = db.Column(db.Float, default=0.0, nullable=False)
    odometer_reading_km = db.Column(db.Float, nullable=False)
    
    scheduled_date = db.Column(db.DateTime, nullable=False)
    completed_date = db.Column(db.DateTime, nullable=True)


class FuelLog(db.Model, BaseModelMixin):
    """Vehicle fuel refill and consumption efficiency record."""
    __tablename__ = 'fuel_logs'

    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False, index=True)
    liters_filled = db.Column(db.Float, nullable=False)
    cost_per_liter_inr = db.Column(db.Float, default=98.50, nullable=False)
    total_cost_inr = db.Column(db.Float, nullable=False)
    odometer_reading_km = db.Column(db.Float, nullable=False)
    
    calculated_km_per_liter = db.Column(db.Float, default=4.2, nullable=False)
    fuel_station = db.Column(db.String(120), default="Autonagar Depot Fuel Station", nullable=False)
    logged_by = db.Column(db.String(120), default="Depot Supervisor", nullable=False)
    filled_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
