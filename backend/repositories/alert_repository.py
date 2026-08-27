"""
CityBus Enterprise Platform - Alert & Service Advisory Repository
File: backend/repositories/alert_repository.py

Encapsulates data operations for municipal service disruptions, delays,
detours, route maintenance bulletins, and passenger advisory broadcasts.
"""

from datetime import datetime
from models import db, Alert
from sqlalchemy import or_, desc


class AlertRepository:
    """Data access layer for municipal transit service alerts."""

    @staticmethod
    def get_all(active_only=False, route_id=None, severity=None, page=1, per_page=20):
        """Fetches service alerts with filtering and pagination."""
        query = Alert.query
        
        if active_only:
            query = query.filter_by(is_active=True)
        if route_id:
            query = query.filter_by(route_id=route_id)
        if severity:
            query = query.filter_by(severity=severity)
            
        total = query.count()
        alerts = query.order_by(Alert.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
        return alerts, total

    @staticmethod
    def get_by_id(alert_id):
        """Fetches alert by ID."""
        return Alert.query.get(alert_id)

    @staticmethod
    def create(title, description, severity="Warning", alert_type="Delay", route_id=None, stop_id=None, is_active=True):
        """Creates a new service advisory bulletin."""
        alert = Alert(
            title=title.strip(),
            description=description.strip(),
            severity=severity,
            alert_type=alert_type,
            route_id=route_id,
            stop_id=stop_id,
            is_active=is_active,
            created_at=datetime.utcnow()
        )
        db.session.add(alert)
        db.session.commit()
        return alert

    @staticmethod
    def update(alert_id, **kwargs):
        """Updates alert advisory attributes."""
        alert = Alert.query.get(alert_id)
        if not alert:
            return None
        for key, val in kwargs.items():
            if hasattr(alert, key) and key != 'id':
                setattr(alert, key, val)
        db.session.commit()
        return alert

    @staticmethod
    def toggle_active(alert_id, is_active=None):
        """Toggles or sets the active status of an alert."""
        alert = Alert.query.get(alert_id)
        if not alert:
            return None
        alert.is_active = not alert.is_active if is_active is None else is_active
        db.session.commit()
        return alert

    @staticmethod
    def delete(alert_id):
        """Deletes a service advisory."""
        alert = Alert.query.get(alert_id)
        if not alert:
            return False
        db.session.delete(alert)
        db.session.commit()
        return True
