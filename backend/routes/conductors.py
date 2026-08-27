"""
CityBus Enterprise Platform - Conductor Management API
File: backend/routes/conductors.py

Provides fare conductor administration, ticket scanning metrics,
cash fare accounting, and vehicle duty roster associations.
"""

from flask import Blueprint, request, jsonify
from repositories.conductor_repository import ConductorRepository
from repositories.audit_repository import AuditRepository
from models import Conductor, db

conductors_bp = Blueprint('conductors_v1', __name__, url_prefix='/api/v1/conductors')


@conductors_bp.route('', methods=['GET'])
def get_conductors():
    """Lists conductors with status filtering, search query, and pagination."""
    try:
        status = request.args.get('status')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        conductors, total = ConductorRepository.get_all(status, search, page, per_page)
        
        return jsonify({
            "success": True,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "conductors": [c.to_dict() for c in conductors]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@conductors_bp.route('/<int:conductor_id>', methods=['GET'])
def get_conductor_details(conductor_id):
    """Fetches details for a single conductor including ticket validation metrics."""
    try:
        conductor = ConductorRepository.get_by_id(conductor_id)
        if not conductor:
            return jsonify({"success": False, "message": "Conductor not found"}), 404
            
        summary = ConductorRepository.get_validation_summary(conductor_id)
        return jsonify({
            "success": True,
            "conductor": conductor.to_dict(),
            "summary": summary
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@conductors_bp.route('', methods=['POST'])
def create_conductor():
    """Registers a new transit conductor."""
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        badge_id = data.get('badge_id', '').strip()
        status = data.get('status', 'Active')

        if not name or not phone or not badge_id:
            return jsonify({"success": False, "message": "Name, phone, and badge ID are required"}), 400

        conductor = ConductorRepository.create(name, phone, badge_id, status)
        AuditRepository.log_event("CONDUCTOR_CREATED", "Conductor", conductor.id, None, request.remote_addr)

        return jsonify({
            "success": True,
            "message": "Conductor registered successfully",
            "conductor": conductor.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@conductors_bp.route('/<int:conductor_id>', methods=['PUT'])
def update_conductor(conductor_id):
    """Updates conductor attributes."""
    try:
        data = request.get_json() or {}
        conductor = ConductorRepository.update(conductor_id, **data)
        if not conductor:
            return jsonify({"success": False, "message": "Conductor not found"}), 404

        AuditRepository.log_event("CONDUCTOR_UPDATED", "Conductor", conductor_id, None, request.remote_addr)
        return jsonify({"success": True, "message": "Conductor updated", "conductor": conductor.to_dict()}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@conductors_bp.route('/<int:conductor_id>', methods=['DELETE'])
def delete_conductor(conductor_id):
    """Deletes a conductor profile."""
    try:
        success, err = ConductorRepository.delete(conductor_id)
        if not success:
            return jsonify({"success": False, "message": err or "Failed to delete"}), 400

        AuditRepository.log_event("CONDUCTOR_DELETED", "Conductor", conductor_id, None, request.remote_addr)
        return jsonify({"success": True, "message": "Conductor deleted successfully"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
