"""
CityBus Enterprise Public Transportation Platform
Main Flask Application Entrypoint (backend/app.py)

Configures SQLAlchemy, Flask-CORS, Flask-SocketIO, registers all API Blueprints,
and starts the real-time server on http://127.0.0.1:5000.
"""

import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db
from websocket.socket_manager import init_socketio

# Blueprints
from routes.auth import auth_bp
from routes.users import users_bp
from routes.drivers import drivers_bp
from routes.conductors import conductors_bp
from routes.buses import buses_bp
from routes.routes import routes_bp
from routes.stops import stops_bp
from routes.trips import trips_bp
from routes.telemetry import telemetry_bp
from routes.eta import eta_bp
from routes.tickets import tickets_bp
from routes.payments import payments_bp
from routes.incidents import incidents_bp
from routes.alerts import alerts_bp
from routes.notifications import notifications_bp
from routes.maintenance import maintenance_bp
from routes.fuel import fuel_bp
from routes.analytics import analytics_bp
from routes.audit import audit_bp
from routes.drts import drts_bp
from routes.afc import afc_bp
from routes.depot import depot_bp
from routes.esg import esg_bp
from routes.feedback import feedback_bp
from routes.lost_found import lost_found_bp
from routes.multimodal import multimodal_bp
from routes.clearinghouse import clearinghouse_bp
from routes.safety_audit import safety_audit_bp
from routes.timetable import timetable_bp
from routes.crew_fatigue import crew_fatigue_bp
from routes.spare_parts import spare_parts_bp
from routes.accessibility import accessibility_bp
from routes.surge_pricing import surge_bp
from routes.weather import weather_bp
from routes.predictive_maintenance import predictive_maint_bp
from routes.detours import detours_bp
from routes.kiosk import kiosk_bp
from routes.fare_evasion import fare_evasion_bp
from routes.depreciation import depreciation_bp
from routes.air_quality import air_quality_bp
from routes.station_lighting import station_lighting_bp
from routes.ticket_recovery import ticket_recovery_bp
from routes.emergency_dispatch import emergency_dispatch_bp
from routes.simulation import simulation_bp
from routes.health import health_bp
from routes.docs import docs_bp
from routes.legacy_api import legacy_bp


def create_app(config_class=Config):
    """Application factory for CityBus Enterprise Engine."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Cross-Origin Resource Sharing (CORS)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Bind SQLAlchemy
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Seed initial demo dataset if database is freshly created and not testing
        if not app.config.get('TESTING'):
            from seeds.seed_data import seed_enterprise_dataset
            seed_enterprise_dataset()

    # Register API Blueprints
    app.register_blueprint(legacy_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(conductors_bp)
    app.register_blueprint(buses_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(stops_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(telemetry_bp)
    app.register_blueprint(eta_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(fuel_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(drts_bp)
    app.register_blueprint(afc_bp)
    app.register_blueprint(depot_bp)
    app.register_blueprint(esg_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(lost_found_bp)
    app.register_blueprint(multimodal_bp)
    app.register_blueprint(clearinghouse_bp)
    app.register_blueprint(safety_audit_bp)
    app.register_blueprint(timetable_bp)
    app.register_blueprint(crew_fatigue_bp)
    app.register_blueprint(spare_parts_bp)
    app.register_blueprint(accessibility_bp)
    app.register_blueprint(surge_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(predictive_maint_bp)
    app.register_blueprint(detours_bp)
    app.register_blueprint(kiosk_bp)
    app.register_blueprint(fare_evasion_bp)
    app.register_blueprint(depreciation_bp)
    app.register_blueprint(air_quality_bp)
    app.register_blueprint(station_lighting_bp)
    app.register_blueprint(ticket_recovery_bp)
    app.register_blueprint(emergency_dispatch_bp)
    app.register_blueprint(simulation_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(docs_bp)

    # Root Welcome Route
    @app.route('/')
    def root():
        return jsonify({
            "name": "CityBus Enterprise Public Transportation Platform API",
            "version": "2.0.0",
            "city": "Vijayawada & Amaravati Capital Region",
            "status": "Online",
            "endpoints": [
                "/api/buses", "/api/routes", "/api/stops", "/api/trips",
                "/api/v1/auth", "/api/v1/buses", "/api/v1/routes",
                "/api/v1/stops", "/api/v1/trips", "/api/v1/tickets",
                "/api/v1/payments", "/api/v1/incidents", "/api/v1/alerts",
                "/api/v1/maintenance", "/api/v1/fuel", "/api/v1/analytics",
                "/api/v1/simulation", "/api/v1/users", "/api/v1/drivers",
                "/api/v1/conductors", "/api/v1/telemetry", "/api/v1/eta",
                "/api/v1/notifications", "/api/v1/audit"
            ],
            "documentation": "/api/v1/docs",
            "health": "/health"
        }), 200

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "message": "Resource or endpoint not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"success": False, "message": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"success": False, "message": "Internal server error occurred"}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        return jsonify({"success": False, "message": str(error)}), 500


    # Bind Socket.IO
    init_socketio(app)

    return app


app = create_app()

if __name__ == '__main__':
    print("=" * 70)
    print("CityBus Enterprise Intelligent Transit Server")
    print("Vijayawada Transit Network & Real-Time Telemetry Pipeline")
    print("Listening on http://127.0.0.1:5000")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
# Feature: API Enhancement
