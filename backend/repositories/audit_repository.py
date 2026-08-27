"""
CityBus Enterprise Platform - Audit Log Repository
File: backend/repositories/audit_repository.py

Provides immutable, secure audit log persistence for security compliance,
administrative changes, user logins, and operational dispatch triggers.
"""

from datetime import datetime
from models import db, AuditLog
from sqlalchemy import or_, desc


class AuditRepository:
    """Data access layer for immutable platform audit trails."""

    @staticmethod
    def log_event(action, entity, entity_id=None, user_id=None, ip_address=None, metadata_json=None):
        """Records a new operational or security audit log entry."""
        log = AuditLog(
            action=action.strip(),
            entity=entity.strip(),
            entity_id=str(entity_id) if entity_id is not None else None,
            user_id=user_id,
            ip_address=ip_address,
            metadata_json=metadata_json,
            timestamp=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def get_logs(entity=None, action=None, user_id=None, search=None, start_date=None, end_date=None, page=1, per_page=50):
        """Queries audit trail records with multi-criteria filtering and pagination."""
        query = AuditLog.query
        
        if entity:
            query = query.filter_by(entity=entity)
        if action:
            query = query.filter_by(action=action)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        if search:
            s = f"%{search}%"
            query = query.filter(or_(
                AuditLog.action.ilike(s),
                AuditLog.entity.ilike(s),
                AuditLog.ip_address.ilike(s)
            ))
            
        total = query.count()
        logs = query.order_by(AuditLog.timestamp.desc()).offset((page - 1) * per_page).limit(per_page).all()
        return logs, total

    @staticmethod
    def get_user_activity(user_id, limit=20):
        """Fetches the latest activities recorded for a particular user."""
        return AuditLog.query.filter_by(user_id=user_id).order_by(AuditLog.timestamp.desc()).limit(limit).all()
