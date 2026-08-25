"""
CityBus Enterprise Platform - Fuel Management API
File: backend/routes/fuel.py
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from repositories.incident_repository import IncidentRepository
from models import db, FuelLog

fuel_bp = Blueprint('fuel_v1', __name__, url_prefix='/api/v1/fuel')


@fuel_bp.route('', methods=['GET'])
def get_fuel_logs():
    """Lists vehicle fuel refill logs."""
    try:
        logs = IncidentRepository.get_fuel_logs()
        return jsonify({
            "success": True,
            "count": len(logs),
            "fuel_logs": [f.to_dict() for f in logs]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@fuel_bp.route('', methods=['POST'])
def add_fuel_log():
    """Records a new fuel refill transaction."""
    try:
        data = request.get_json() or {}
        bus_id = data.get('bus_id')
        liters = float(data.get('liters_filled', 50.0))
        cost_per_liter = float(data.get('cost_per_liter', 98.50))
        odometer = float(data.get('odometer_km', 1000.0))
        station = data.get('fuel_station', 'PNBS Central Fuel Depot')
        logged_by = data.get('logged_by', 'Depot In-Charge')

        if not bus_id:
            return jsonify({"success": False, "message": "Missing bus_id"}), 400

        total_cost = liters * cost_per_liter
        km_per_liter = 4.2 # calculated average for city express bus

        log = FuelLog(
            bus_id=bus_id,
            liters_filled=liters,
            cost_per_liter_inr=cost_per_liter,
            total_cost_inr=total_cost,
            odometer_reading_km=odometer,
            calculated_km_per_liter=km_per_liter,
            fuel_station=station,
            logged_by=logged_by,
            filled_at=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Fuel refill recorded",
            "fuel_log": log.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
