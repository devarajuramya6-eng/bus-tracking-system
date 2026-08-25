"""
CityBus Enterprise Platform - OpenAPI & Swagger Specification Endpoint
File: backend/routes/docs.py
"""

from flask import Blueprint, jsonify

docs_bp = Blueprint('docs_v1', __name__, url_prefix='/api/v1')


@docs_bp.route('/docs', methods=['GET'])
def get_api_documentation():
    """Returns OpenAPI 3.0 Specification for CityBus API."""
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "CityBus Enterprise Public Transit Platform API",
            "version": "2.0.0",
            "description": "Comprehensive REST and Real-Time WebSocket API for municipal fleet tracking, journey planning, ticketing, QR validation, dispatcher command center, and transit telemetry."
        },
        "servers": [
            { "url": "http://127.0.0.1:5000/api/v1", "description": "Local Development Server" }
        ],
        "endpoints": {
            "auth": {
                "login": "POST /auth/login - JWT authentication",
                "register": "POST /auth/register - User registration",
                "refresh": "POST /auth/refresh - Token refresh",
                "me": "GET /auth/me - Current user profile"
            },
            "buses": {
                "list": "GET /buses - List all buses with status filter",
                "single": "GET /buses/{id} - Single bus telemetry & calculated ETA",
                "nearby": "GET /buses/nearby?lat=...&lng=... - Proximity sorted buses",
                "update_location": "POST /buses/location - Live GPS telemetry ping"
            },
            "routes": {
                "list": "GET /routes - All transit corridors",
                "single": "GET /routes/{id} - Route geometry & ordered stops"
            },
            "stops": {
                "list": "GET /stops - All city transit stops",
                "single": "GET /stops/{id} - Stop details and next departures"
            },
            "trips": {
                "list": "GET /trips - Active and historical trips",
                "start": "POST /trips/start - Start driver trip",
                "stop": "POST /trips/stop - End driver trip"
            },
            "tickets": {
                "create": "POST /tickets - Book ticket & generate QR",
                "validate": "POST /tickets/validate - Conductor QR validation",
                "user_history": "GET /tickets/user/{userId} - Passenger digital wallet"
            },
            "payments": {
                "order": "POST /payments/order - Create Razorpay order",
                "verify": "POST /payments/verify - Verify digital signature"
            },
            "incidents": {
                "list": "GET /incidents - Operational incident list",
                "report": "POST /incidents - Report breakdown/traffic/accident",
                "sos": "POST /incidents/emergency/sos - Emergency panic trigger",
                "update_status": "PATCH /incidents/{id}/status - Kanban status transition"
            },
            "alerts": {
                "list": "GET /alerts - Active service disruption alerts",
                "broadcast": "POST /alerts - Broadcast service alert"
            },
            "maintenance": {
                "list": "GET /maintenance - Work orders and service intervals",
                "create": "POST /maintenance - Create work order"
            },
            "fuel": {
                "list": "GET /fuel - Fuel refill transactions and efficiency",
                "log": "POST /fuel - Record fuel refill"
            },
            "analytics": {
                "summary": "GET /analytics/summary - KPI summary cards",
                "ridership": "GET /analytics/ridership - Weekly demand trends"
            },
            "health": {
                "health": "GET /health - System health status",
                "live": "GET /health/live - Liveness probe",
                "ready": "GET /health/ready - Readiness probe"
            }
        }
    }), 200
