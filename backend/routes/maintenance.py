"""
CityBus Enterprise Platform - Maintenance & Work Orders API
File: backend/routes/maintenance.py
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from repositories.incident_repository import IncidentRepository
from models import db, MaintenanceWorkOrder

maintenance_bp = Blueprint('maintenance_v1', __name__, url_prefix='/api/v1/maintenance')


@maintenance_bp.route('', methods=['GET'])
def get_work_orders():
    """Lists maintenance work orders."""
    try:
        orders = IncidentRepository.get_maintenance_work_orders()
        return jsonify({
            "success": True,
            "count": len(orders),
            "work_orders": [o.to_dict() for o in orders]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@maintenance_bp.route('', methods=['POST'])
def create_work_order():
    """Creates a new maintenance work order."""
    try:
        data = request.get_json() or {}
        bus_id = data.get('bus_id')
        service_type = data.get('service_type', 'Scheduled Inspection')
        technician = data.get('technician_name', 'Workshop Lead')
        description = data.get('description', 'Routine periodic maintenance')
        cost = float(data.get('cost_inr', 0.0))
        odometer = float(data.get('odometer_km', 1000.0))
        priority = data.get('priority', 'Medium')

        if not bus_id:
            return jsonify({"success": False, "message": "Missing bus_id"}), 400

        order_num = f"WO-{datetime.utcnow().strftime('%y%m%d')}-{datetime.utcnow().strftime('%H%M%S')}"
        order = MaintenanceWorkOrder(
            work_order_number=order_num,
            bus_id=bus_id,
            service_type=service_type,
            technician_name=technician,
            description=description,
            cost_inr=cost,
            odometer_reading_km=odometer,
            priority=priority,
            status="In Progress",
            scheduled_date=datetime.utcnow()
        )
        db.session.add(order)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Work order created",
            "work_order": order.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
