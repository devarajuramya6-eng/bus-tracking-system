"""
CityBus Enterprise Platform - Real GPS Pipeline & Telemetry Ingestion Service
File: backend/services/gps_service.py
"""

import math
from datetime import datetime
from repositories.bus_repository import BusRepository
from repositories.route_repository import RouteRepository


class GPSService:
    """Handles real-time GPS telemetry validation, geofencing, heading calculations, and stale detection."""

    @staticmethod
    def process_telemetry_ping(bus_id, lat, lng, speed=0.0, heading=None, accuracy=5.0):
        """
        Ingests a live GPS ping from hardware/browser, updates database,
        evaluates geofences for stop arrival, and computes heading.
        """
        bus = BusRepository.get_by_id(bus_id)
        if not bus:
            return None, "Bus not found"

        # If heading not supplied by device, calculate from previous coordinates
        if heading is None or heading == 0.0:
            heading = GPSService.calculate_heading(bus.latitude, bus.longitude, lat, lng)

        # Update position
        updated_bus = BusRepository.update_location(bus_id, lat, lng, speed, heading, accuracy)

        # Check geofencing against assigned route stops
        arrival_event = None
        if updated_bus.route_id:
            arrival_event = GPSService.check_stop_geofence(updated_bus)

        return {
            "bus": updated_bus.to_dict(),
            "arrival_event": arrival_event
        }, None

    @staticmethod
    def calculate_heading(lat1, lon1, lat2, lon2):
        if lat1 == lat2 and lon1 == lon2:
            return 0.0
        dLon = math.radians(lon2 - lon1)
        y = math.sin(dLon) * math.cos(math.radians(lat2))
        x = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - \
            math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(dLon)
        brng = math.atan2(y, x)
        return round((math.degrees(brng) + 360) % 360, 1)

    @staticmethod
    def check_stop_geofence(bus, radius_meters=80.0):
        """Checks if vehicle has entered within radius of any route stop."""
        stops = RouteRepository.get_all_stops(bus.route_id)
        for stop in stops:
            dist_km = BusRepository.haversine_km(bus.latitude, bus.longitude, stop.latitude, stop.longitude)
            if dist_km * 1000 <= radius_meters:
                return {
                    "stop_id": stop.id,
                    "stop_name": stop.name,
                    "stop_code": stop.code,
                    "distance_meters": round(dist_km * 1000, 1)
                }
        return None
