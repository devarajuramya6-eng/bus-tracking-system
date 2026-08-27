"""
CityBus Enterprise Platform - Lost & Found Property API
File: backend/routes/lost_found.py

Provides property catalog search, new found item intake, and passenger claim verification.
"""

from flask import Blueprint, request, jsonify
from services.lost_and_found_service import LostAndFoundService

lost_found_bp = Blueprint('lost_found_v1', __name__, url_prefix='/api/v1/lost-found')


@lost_found_bp.route('/items', methods=['GET'])
def search_lost_items():
    """Searches unclaimed lost property in depot safe."""
    try:
        category = request.args.get('category')
        keyword = request.args.get('keyword')
        items = LostAndFoundService.search_items(category, keyword)
        return jsonify({"success": True, "count": len(items), "items": items}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@lost_found_bp.route('/register', methods=['POST'])
def register_found_item():
    """Logs a new item retrieved from a vehicle."""
    try:
        data = request.get_json() or {}
        bus_id = data.get('bus_id', 1)
        category = data.get('category', 'Electronics')
        description = data.get('description', '').strip()
        found_by = data.get('found_by', 'Conductor Team')

        if not description:
            return jsonify({"success": False, "message": "Description is required"}), 400

        item = LostAndFoundService.register_found_item(bus_id, category, description, found_by)
        return jsonify({"success": True, "item": item}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@lost_found_bp.route('/claim/<int:item_id>', methods=['POST'])
def claim_item(item_id):
    """Processes passenger claim for a lost item."""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 1)
        notes = data.get('notes', 'Claimed with verification')

        success, err = LostAndFoundService.claim_item(item_id, user_id, notes)
        if not success:
            return jsonify({"success": False, "message": err or "Claim failed"}), 400
        return jsonify({"success": True, "message": "Property claim approved"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
