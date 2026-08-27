"""
CityBus Enterprise Platform - Clearinghouse & Settlement API
File: backend/routes/clearinghouse.py

Provides daily ticket clearinghouse ledgers, concession subsidies, and fee reconciliation.
"""

from flask import Blueprint, jsonify
from services.transit_clearinghouse_service import TransitClearinghouseService

clearinghouse_bp = Blueprint('clearinghouse_v1', __name__, url_prefix='/api/v1/clearinghouse')


@clearinghouse_bp.route('/ledger', methods=['GET'])
def get_clearinghouse_ledger():
    """Returns daily revenue reconciliation ledger."""
    try:
        data = TransitClearinghouseService.calculate_daily_settlement_ledger()
        return jsonify({"success": True, "ledger": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
