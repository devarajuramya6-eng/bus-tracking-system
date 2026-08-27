"""
CityBus Enterprise Platform - GTFS Realtime (GTFS-RT) Feed Generator
File: backend/services/gtfs_realtime_generator.py

Produces standardized General Transit Feed Specification Realtime (GTFS-RT) feeds
for third-party transit aggregators (Google Maps Transit, Apple Maps, Transit App):
- FeedMessage: TripUpdates (delay, arrival/departure estimates)
- FeedMessage: VehiclePositions (live coordinates, heading, speed, crowding)
- FeedMessage: Alerts (service advisories, cancellations, detours)
"""

import time
from datetime import datetime
from typing import Dict, List, Any
from models import Bus, Route, Trip, Alert, db


class GTFSRealtimeGenerator:
    """Serializes live platform state into GTFS-RT compliant JSON feeds."""

    FEED_VERSION = "2.0"

    @staticmethod
    def generate_vehicle_positions_feed() -> Dict[str, Any]:
        """Generates GTFS-RT VehiclePositions entity array."""
        buses = Bus.query.filter_by(status='On Route').all()
        entities = []

        for bus in buses:
            entities.append({
                "id": f"VP_{bus.id}_{int(time.time())}",
                "is_deleted": False,
                "vehicle": {
                    "trip": {
                        "trip_id": str(bus.get_active_trip_id() or f"TRIP_{bus.id}"),
                        "route_id": str(bus.route_id or "1"),
                        "start_time": datetime.utcnow().strftime("%H:%M:%S"),
                        "schedule_relationship": "SCHEDULED"
                    },
                    "vehicle": {
                        "id": str(bus.id),
                        "label": bus.bus_number,
                        "license_plate": bus.registration_plate or f"AP-16-{bus.id}"
                    },
                    "position": {
                        "latitude": round(bus.latitude, 6),
                        "longitude": round(bus.longitude, 6),
                        "bearing": round(bus.heading, 1),
                        "speed": round(bus.speed / 3.6, 2) # Converted to m/s
                    },
                    "occupancy_status": GTFSRealtimeGenerator._get_occupancy_enum(bus.occupancy, bus.capacity),
                    "timestamp": int(bus.last_gps_update.timestamp()) if bus.last_gps_update else int(time.time())
                }
            })

        return {
            "header": {
                "gtfs_realtime_version": GTFSRealtimeGenerator.FEED_VERSION,
                "incrementality": "FULL_DATASET",
                "timestamp": int(time.time())
            },
            "entity": entities
        }

    @staticmethod
    def generate_trip_updates_feed() -> Dict[str, Any]:
        """Generates GTFS-RT TripUpdates entity array with estimated delays."""
        active_trips = Trip.query.filter_by(status='Active').all()
        entities = []

        for trip in active_trips:
            delay_sec = 180 if (trip.bus_rel and trip.bus_rel.status == 'Delayed') else 0
            entities.append({
                "id": f"TU_{trip.id}",
                "is_deleted": False,
                "trip_update": {
                    "trip": {
                        "trip_id": str(trip.id),
                        "route_id": str(trip.route_id),
                        "schedule_relationship": "SCHEDULED"
                    },
                    "vehicle": {
                        "id": str(trip.bus_id),
                        "label": trip.bus_rel.bus_number if trip.bus_rel else "Bus"
                    },
                    "delay": delay_sec,
                    "timestamp": int(time.time())
                }
            })

        return {
            "header": {
                "gtfs_realtime_version": GTFSRealtimeGenerator.FEED_VERSION,
                "incrementality": "FULL_DATASET",
                "timestamp": int(time.time())
            },
            "entity": entities
        }

    @staticmethod
    def generate_alerts_feed() -> Dict[str, Any]:
        """Generates GTFS-RT ServiceAlerts entity array."""
        alerts = Alert.query.filter_by(is_active=True).all()
        entities = []

        for alert in alerts:
            entities.append({
                "id": f"ALERT_{alert.id}",
                "is_deleted": False,
                "alert": {
                    "active_period": [{
                        "start": int(alert.created_at.timestamp()) if alert.created_at else int(time.time())
                    }],
                    "informed_entity": [{
                        "route_id": str(alert.route_id) if alert.route_id else None,
                        "stop_id": str(alert.stop_id) if alert.stop_id else None
                    }],
                    "cause": "UNKNOWN_CAUSE",
                    "effect": "SIGNIFICANT_DELAYS" if alert.severity == "High" else "MODIFIED_SERVICE",
                    "header_text": {
                        "translation": [{"text": alert.title, "language": "en"}]
                    },
                    "description_text": {
                        "translation": [{"text": alert.description, "language": "en"}]
                    }
                }
            })

        return {
            "header": {
                "gtfs_realtime_version": GTFSRealtimeGenerator.FEED_VERSION,
                "incrementality": "FULL_DATASET",
                "timestamp": int(time.time())
            },
            "entity": entities
        }

    @staticmethod
    def _get_occupancy_enum(occupancy: int, capacity: int) -> str:
        """Maps passenger count to GTFS-RT OccupancyStatus enum."""
        if not capacity or capacity <= 0:
            return "NO_DATA_AVAILABLE"
        ratio = occupancy / float(capacity)
        if ratio < 0.3:
            return "MANY_SEATS_AVAILABLE"
        elif ratio < 0.7:
            return "FEW_SEATS_AVAILABLE"
        elif ratio < 0.95:
            return "STANDING_ROOM_ONLY"
        else:
            return "FULL"
