"""
CityBus Enterprise Platform - Incident Repository
File: backend/repositories/incident_repository.py
"""

from datetime import datetime
from models import db, Incident, Alert, MaintenanceWorkOrder, FuelLog, AuditLog


class IncidentRepository:
    """Isolates database operations for Incidents, Alerts, Maintenance, and Fuel."""

    @staticmethod
    def get_all_incidents(status=None, limit=100):
        query = Incident.query
        if status and status != 'All':
            query = query.filter_by(status=status)
        return query.order_by(Incident.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_incident_by_id(incident_id):
        return Incident.query.get(incident_id)

    @staticmethod
    def create_incident(incident_type, title, description, severity="Medium", bus_id=None, driver_id=None, route_id=None, lat=None, lng=None, reported_by=None):
        incident_num = Incident.generate_incident_number()
        incident = Incident(
            incident_number=incident_num,
            incident_type=incident_type,
            severity=severity,
            status="New",
            title=title,
            description=description,
            bus_id=bus_id,
            driver_id=driver_id,
            route_id=route_id,
            latitude=lat,
            longitude=lng,
            reported_by_user_id=reported_by
        )
        db.session.add(incident)
        db.session.commit()
        return incident

    @staticmethod
    def update_incident_status(incident_id, status, resolution_notes=None, dispatcher=None):
        inc = Incident.query.get(incident_id)
        if inc:
            inc.status = status
            if resolution_notes:
                inc.resolution_notes = resolution_notes
            if dispatcher:
                inc.assigned_dispatcher = dispatcher
            if status in ['Resolved', 'Closed']:
                inc.resolved_at = datetime.utcnow()
            db.session.commit()
        return inc

    @staticmethod
    def get_active_alerts():
        return Alert.query.filter_by(is_active=True).order_by(Alert.start_time.desc()).all()

    @staticmethod
    def create_alert(title, description, severity="Warning", target_scope="All", target_route_id=None):
        alert = Alert(
            title=title,
            description=description,
            severity=severity,
            target_scope=target_scope,
            target_route_id=target_route_id,
            is_active=True
        )
        db.session.add(alert)
        db.session.commit()
        return alert

    @staticmethod
    def get_maintenance_work_orders():
        return MaintenanceWorkOrder.query.order_by(MaintenanceWorkOrder.scheduled_date.desc()).all()

    @staticmethod
    def get_fuel_logs():
        return FuelLog.query.order_by(FuelLog.filled_at.desc()).all()
