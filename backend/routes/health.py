"""
CityBus Enterprise Platform - Health & Diagnostics API
File: backend/routes/health.py
"""

from datetime import datetime
from flask import Blueprint, jsonify
from models import db, Bus

health_bp = Blueprint('health_v1', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """General health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "CityBus Enterprise Transit Engine",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


@health_bp.route('/health/live', methods=['GET'])
def liveness():
    """Kubernetes / Docker Liveness probe."""
    return jsonify({ "status": "alive" }), 200


@health_bp.route('/health/ready', methods=['GET'])
def readiness():
    """Kubernetes / Docker Readiness probe verifying database connectivity."""
    try:
        # Check DB connection
        db.session.execute(db.text('SELECT 1'))
        total_buses = Bus.query.count()
        return jsonify({
            "status": "ready",
            "database": "connected",
            "active_fleet_count": total_buses,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "not_ready",
            "database": "error",
            "error": str(e)
        }), 503
