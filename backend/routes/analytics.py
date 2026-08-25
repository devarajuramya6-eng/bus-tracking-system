"""
CityBus Enterprise Platform - Analytics & Reports API
File: backend/routes/analytics.py
"""

from flask import Blueprint, jsonify
from services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics_v1', __name__, url_prefix='/api/v1/analytics')


@analytics_bp.route('/summary', methods=['GET'])
def get_summary():
    """Returns transit KPI summary cards."""
    try:
        data = AnalyticsService.get_kpi_summary()
        return jsonify({
            "success": True,
            "data": data
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@analytics_bp.route('/ridership', methods=['GET'])
def get_ridership():
    """Returns weekly ridership and revenue aggregates."""
    try:
        data = AnalyticsService.get_weekly_ridership()
        return jsonify({
            "success": True,
            "data": data
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
