"""
CityBus Enterprise Platform - Telemetry Repository
File: backend/repositories/telemetry_repository.py

Manages high-frequency GPS coordinate logs, breadcrumb trails,
speed traces, and historical vehicle trajectory records.
"""

from datetime import datetime, timedelta
from models import db, Telemetry, Bus
from sqlalchemy import desc


class TelemetryRepository:
    """Data access layer for high-throughput vehicle telemetry."""

    @staticmethod
    def record_ping(bus_id, latitude, longitude, speed=0.0, heading=0.0, accuracy=5.0, trip_id=None, timestamp=None):
        """Appends a new GPS telemetry coordinate breadcrumb."""
        telemetry = Telemetry(
            bus_id=bus_id,
            trip_id=trip_id,
            latitude=float(latitude),
            longitude=float(longitude),
            speed=float(speed),
            heading=float(heading) if heading is not None else 0.0,
            accuracy=float(accuracy) if accuracy is not None else 5.0,
            timestamp=timestamp or datetime.utcnow()
        )
        db.session.add(telemetry)
        db.session.commit()
        return telemetry

    @staticmethod
    def get_recent_trail(bus_id, limit=50):
        """Fetches the latest breadcrumb coordinates for a bus to render historical trails."""
        logs = Telemetry.query.filter_by(bus_id=bus_id).order_by(Telemetry.timestamp.desc()).limit(limit).all()
        # Return in chronological order
        return [log.to_dict() for log in reversed(logs)]

    @staticmethod
    def get_trip_trail(trip_id):
        """Fetches all GPS coordinates recorded during a specific trip."""
        logs = Telemetry.query.filter_by(trip_id=trip_id).order_by(Telemetry.timestamp.asc()).all()
        return [log.to_dict() for log in logs]

    @staticmethod
    def get_bus_telemetry_stats(bus_id, hours=24):
        """Computes average speed, max speed, and total coordinate pings in the last N hours."""
        since = datetime.utcnow() - timedelta(hours=hours)
        logs = Telemetry.query.filter(
            Telemetry.bus_id == bus_id,
            Telemetry.timestamp >= since
        ).all()
        
        if not logs:
            return {
                "bus_id": bus_id,
                "ping_count": 0,
                "max_speed_kmh": 0.0,
                "avg_speed_kmh": 0.0
            }
            
        speeds = [l.speed for l in logs if l.speed is not None]
        max_speed = max(speeds) if speeds else 0.0
        avg_speed = sum(speeds) / max(1, len(speeds))
        
        return {
            "bus_id": bus_id,
            "ping_count": len(logs),
            "max_speed_kmh": round(max_speed, 1),
            "avg_speed_kmh": round(avg_speed, 1),
            "last_ping_time": logs[-1].timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
