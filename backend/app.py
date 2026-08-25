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
from routes.buses import buses_bp
from routes.routes import routes_bp
from routes.stops import stops_bp
from routes.trips import trips_bp
from routes.tickets import tickets_bp
from routes.payments import payments_bp
from routes.incidents import incidents_bp
from routes.alerts import alerts_bp
from routes.maintenance import maintenance_bp
from routes.fuel import fuel_bp
from routes.analytics import analytics_bp
from routes.simulation import simulation_bp
from routes.health import health_bp
from routes.docs import docs_bp


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
        # Seed initial demo dataset if database is freshly created
        from seeds.seed_data import seed_enterprise_dataset
        seed_enterprise_dataset()

    # Register API Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(buses_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(stops_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(fuel_bp)
    app.register_blueprint(analytics_bp)
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
            "documentation": "/api/v1/docs",
            "health": "/health"
        }), 200

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "message": "Resource or endpoint not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"success": False, "message": "Internal server error occurred"}), 500

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
