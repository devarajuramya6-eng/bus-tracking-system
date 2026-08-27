"""
CityBus Enterprise Platform - Fare Evasion Audit API
File: backend/routes/fare_evasion.py

Provides fare evasion audits and leakage detection endpoints.
"""

from flask import Blueprint, request, jsonify
from services.fare_evasion_risk_scorer import FareEvasionRiskScorer

fare_evasion_bp = Blueprint('fare_evasion_v1', __name__, url_prefix='/api/v1/fare-evasion')


@fare_evasion_bp.route('/audit', methods=['POST'])
def audit_fare_evasion():
    """Calculates unpaid passenger count and revenue leakage."""
    try:
        data = request.get_json() or {}
        bus_id = int(data.get('bus_id', 1))
        apc_boardings = int(data.get('apc_boardings', 45))
        validated_tickets = int(data.get('validated_tickets', 38))

        res = FareEvasionRiskScorer.audit_trip_fare_compliance(bus_id, apc_boardings, validated_tickets)
        return jsonify({"success": True, **res}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
