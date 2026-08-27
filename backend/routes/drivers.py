"""
CityBus Enterprise Platform - Driver Management API
File: backend/routes/drivers.py

Provides full driver profile administration, shift assignments,
duty rosters, performance analytics, and active trip tracking.
"""

from flask import Blueprint, request, jsonify
from repositories.driver_repository import DriverRepository
from repositories.audit_repository import AuditRepository
from models import Driver, Trip, Bus, db

drivers_bp = Blueprint('drivers_v1', __name__, url_prefix='/api/v1/drivers')


@drivers_bp.route('', methods=['GET'])
def get_drivers():
    """Lists all drivers with status filtering, search query, and pagination."""
    try:
        status = request.args.get('status')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        drivers, total = DriverRepository.get_all(status, search, page, per_page)
        
        return jsonify({
            "success": True,
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "drivers": [d.to_dict() for d in drivers]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@drivers_bp.route('/<int:driver_id>', methods=['GET'])
def get_driver_details(driver_id):
    """Fetches details for a single driver including statistics and active trip."""
    try:
        driver = DriverRepository.get_by_id(driver_id)
        if not driver:
            return jsonify({"success": False, "message": "Driver not found"}), 404
            
        stats = DriverRepository.get_driver_statistics(driver_id)
        return jsonify({
            "success": True,
            "driver": driver.to_dict(),
            "statistics": stats
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@drivers_bp.route('', methods=['POST'])
def create_driver():
    """Registers a new fleet driver."""
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip() or None
        license_number = data.get('license_number', '').strip() or None
        experience = int(data.get('experience_years', 3))
        rating = float(data.get('rating', 4.8))
        status = data.get('status', 'Active')

        if not name or not phone:
            return jsonify({"success": False, "message": "Name and phone number are required"}), 400

        driver = DriverRepository.create(name, phone, email, license_number, experience, rating, status)
        AuditRepository.log_event("DRIVER_CREATED", "Driver", driver.id, None, request.remote_addr, f"Name: {name}")

        return jsonify({
            "success": True,
            "message": "Driver created successfully",
            "driver": driver.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@drivers_bp.route('/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    """Updates driver attributes."""
    try:
        data = request.get_json() or {}
        driver = DriverRepository.update(driver_id, **data)
        if not driver:
            return jsonify({"success": False, "message": "Driver not found"}), 404

        AuditRepository.log_event("DRIVER_UPDATED", "Driver", driver_id, None, request.remote_addr)
        return jsonify({"success": True, "message": "Driver updated", "driver": driver.to_dict()}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@drivers_bp.route('/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    """Deletes a driver record."""
    try:
        success, err = DriverRepository.delete(driver_id)
        if not success:
            return jsonify({"success": False, "message": err or "Failed to delete"}), 400

        AuditRepository.log_event("DRIVER_DELETED", "Driver", driver_id, None, request.remote_addr)
        return jsonify({"success": True, "message": "Driver deleted successfully"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@drivers_bp.route('/<int:driver_id>/trips', methods=['GET'])
def get_driver_trips(driver_id):
    """Retrieves trip history for a driver."""
    try:
        trips = DriverRepository.get_trip_history(driver_id)
        return jsonify({
            "success": True,
            "count": len(trips),
            "trips": [t.to_dict() for t in trips]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
