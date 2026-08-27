"""
CityBus Enterprise Platform - Safety Audit API
File: backend/routes/safety_audit.py

Provides HOS driver compliance and fleet roadworthiness inspection results.
"""

from flask import Blueprint, jsonify
from services.transit_safety_audit_service import TransitSafetyAuditService

safety_audit_bp = Blueprint('safety_audit_v1', __name__, url_prefix='/api/v1/safety-audit')


@safety_audit_bp.route('/drivers', methods=['GET'])
def get_driver_safety_audit():
    """Returns driver compliance and HOS audit status."""
    try:
        data = TransitSafetyAuditService.audit_driver_safety_compliance()
        return jsonify({"success": True, "driver_audit": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@safety_audit_bp.route('/fleet', methods=['GET'])
def get_fleet_safety_audit():
    """Returns fleet roadworthiness and depot inspection status."""
    try:
        data = TransitSafetyAuditService.audit_fleet_roadworthiness()
        return jsonify({"success": True, "fleet_audit": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
