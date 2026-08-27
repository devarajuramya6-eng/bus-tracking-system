"""
CityBus Enterprise Platform - Spare Parts Inventory API
File: backend/routes/spare_parts.py

Provides warehouse stock levels, part consumption for work orders, and restocking endpoints.
"""

from flask import Blueprint, request, jsonify
from services.depot_spare_parts_inventory_service import DepotSparePartsInventoryService

spare_parts_bp = Blueprint('spare_parts_v1', __name__, url_prefix='/api/v1/spare-parts')


@spare_parts_bp.route('/inventory', methods=['GET'])
def get_inventory():
    """Returns spare parts stock catalog."""
    try:
        parts = DepotSparePartsInventoryService.get_all_parts()
        return jsonify({"success": True, "parts": parts}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@spare_parts_bp.route('/consume', methods=['POST'])
def consume_part():
    """Deducts spare parts for a maintenance work order."""
    try:
        data = request.get_json() or {}
        part_id = data.get('part_id')
        qty = int(data.get('quantity', 1))
        order_id = int(data.get('work_order_id', 1))

        if not part_id:
            return jsonify({"success": False, "message": "part_id is required"}), 400

        success, err = DepotSparePartsInventoryService.consume_part_for_work_order(part_id, qty, order_id)
        if not success:
            return jsonify({"success": False, "message": err}), 400

        return jsonify({"success": True, "message": f"Consumed {qty} of {part_id}"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
