"""
CityBus Enterprise Platform - Depot Operations API
File: backend/routes/depot.py

Provides depot parking bay visualizer, EV charger monitoring, and check-in slot allocation.
"""

from flask import Blueprint, request, jsonify
from services.depot_operations_service import DepotOperationsService

depot_bp = Blueprint('depot_v1', __name__, url_prefix='/api/v1/depot')


@depot_bp.route('/yard', methods=['GET'])
def get_yard_map():
    """Returns visual topology matrix of depot parking bays and EV charging bays."""
    try:
        data = DepotOperationsService.get_yard_occupancy_matrix()
        return jsonify({"success": True, **data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@depot_bp.route('/check-in', methods=['POST'])
def vehicle_check_in():
    """Assigns optimal bay to a bus returning to depot."""
    try:
        data = request.get_json() or {}
        bus_id = data.get('bus_id')
        if not bus_id:
            return jsonify({"success": False, "message": "bus_id is required"}), 400

        slot_id, err = DepotOperationsService.assign_vehicle_to_bay(bus_id)
        if err:
            return jsonify({"success": False, "message": err}), 400

        return jsonify({
            "success": True,
            "message": f"Bus assigned to {slot_id}",
            "slot_id": slot_id,
            "bus_id": bus_id
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@depot_bp.route('/release/<slot_id>', methods=['POST'])
def release_bay(slot_id):
    """Releases a parking slot for morning departure."""
    try:
        success = DepotOperationsService.release_bay(slot_id)
        if not success:
            return jsonify({"success": False, "message": "Bay not found"}), 404
        return jsonify({"success": True, "message": f"Bay {slot_id} released"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
