"""
CityBus Enterprise Platform - Audit Logs API
File: backend/routes/audit.py

Provides read-only access to immutable system audit logs for administrative
compliance, security auditing, and forensics.
"""

from flask import Blueprint, request, jsonify
from repositories.audit_repository import AuditRepository
from models import AuditLog, db

audit_bp = Blueprint('audit_v1', __name__, url_prefix='/api/v1/audit')


@audit_bp.route('', methods=['GET'])
def get_audit_logs():
    """Lists audit logs with multi-field filtering and pagination."""
    try:
        entity = request.args.get('entity')
        action = request.args.get('action')
        user_id = request.args.get('user_id', type=int)
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))

        logs, total = AuditRepository.get_logs(entity, action, user_id, search, None, None, page, per_page)

        return jsonify({
            "success": True,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "logs": [log.to_dict() for log in logs]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@audit_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_audit_trail(user_id):
    """Fetches the recent activity trail for a single user."""
    try:
        limit = int(request.args.get('limit', 25))
        logs = AuditRepository.get_user_activity(user_id, limit)
        return jsonify({
            "success": True,
            "user_id": user_id,
            "count": len(logs),
            "logs": [log.to_dict() for log in logs]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
