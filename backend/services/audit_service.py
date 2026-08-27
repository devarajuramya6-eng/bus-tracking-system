"""
CityBus Enterprise Platform - Audit Service
File: backend/services/audit_service.py

Orchestrates automated audit log capture for critical state modifications,
security authorization checks, financial transactions, and GPS anomalies.
"""

from typing import Dict, List, Any, Optional
from repositories.audit_repository import AuditRepository
from models import AuditLog, db


class AuditService:
    """Business service for enterprise compliance and audit trail management."""

    @staticmethod
    def record_access_event(user_id: int, action: str, ip_address: Optional[str] = None, success: bool = True):
        """Logs user authentication and session events (login, logout, token refresh)."""
        status_text = "SUCCESS" if success else "FAILED"
        AuditRepository.log_event(
            action=f"AUTH_{action.upper()}_{status_text}",
            entity="AuthSession",
            entity_id=str(user_id),
            user_id=user_id,
            ip_address=ip_address
        )

    @staticmethod
    def record_entity_mutation(action: str, entity_name: str, entity_id: Any, user_id: Optional[int] = None,
                               ip_address: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """Records create/update/delete operations on transit domain entities."""
        import json
        meta_str = json.dumps(metadata) if metadata else None
        AuditRepository.log_event(
            action=action.upper(),
            entity=entity_name,
            entity_id=str(entity_id),
            user_id=user_id,
            ip_address=ip_address,
            metadata_json=meta_str
        )

    @staticmethod
    def get_audit_report(entity: Optional[str] = None, action: Optional[str] = None,
                         user_id: Optional[int] = None, search: Optional[str] = None,
                         page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """Fetches structured audit logs with summary statistics."""
        logs, total = AuditRepository.get_logs(
            entity=entity,
            action=action,
            user_id=user_id,
            search=search,
            page=page,
            per_page=per_page
        )
        return {
            "success": True,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "logs": [l.to_dict() for l in logs]
        }
