"""
CityBus Enterprise Platform - Dead Reckoning & Map Matching Engine
File: backend/services/dead_reckoning_engine.py

Interpolates expected vehicle position along route segments when GPS signals drop
in tunnels, urban canyons, or overpasses using speed, heading, and elapsed time.
"""

import math
from datetime import datetime
from typing import Tuple, List, Optional, Dict, Any


class DeadReckoningEngine:
    """Estimates missing vehicle coordinates along assigned route paths."""

    EARTH_RADIUS_KM = 6371.0

    @staticmethod
    def project_coordinate(lat: float, lng: float, speed_kmh: float, heading_deg: float, elapsed_seconds: float) -> Tuple[float, float]:
        """
        Projects next latitude/longitude given starting position, speed, heading, and elapsed time.
        """
        if elapsed_seconds <= 0 or speed_kmh <= 0:
            return lat, lng

        # Distance traveled in kilometers
        distance_km = (speed_kmh / 3600.0) * elapsed_seconds
        bearing_rad = math.radians(heading_deg)
        lat_rad = math.radians(lat)
        lng_rad = math.radians(lng)

        new_lat_rad = math.asin(
            math.sin(lat_rad) * math.cos(distance_km / DeadReckoningEngine.EARTH_RADIUS_KM) +
            math.cos(lat_rad) * math.sin(distance_km / DeadReckoningEngine.EARTH_RADIUS_KM) * math.cos(bearing_rad)
        )

        new_lng_rad = lng_rad + math.atan2(
            math.sin(bearing_rad) * math.sin(distance_km / DeadReckoningEngine.EARTH_RADIUS_KM) * math.cos(lat_rad),
            math.cos(distance_km / DeadReckoningEngine.EARTH_RADIUS_KM) - math.sin(lat_rad) * math.sin(new_lat_rad)
        )

        return round(math.degrees(new_lat_rad), 6), round(math.degrees(new_lng_rad), 6)

    @staticmethod
    def snap_to_route(current_lat: float, current_lng: float, route_waypoints: List[List[float]]) -> Tuple[float, float, float]:
        """
        Finds the closest point on the route polyline (Map Matching).
        Returns (snapped_lat, snapped_lng, distance_meters).
        """
        if not route_waypoints:
            return current_lat, current_lng, 0.0

        min_dist = float('inf')
        closest_pt = (current_lat, current_lng)

        for wp in route_waypoints:
            d = DeadReckoningEngine.distance_meters(current_lat, current_lng, wp[0], wp[1])
            if d < min_dist:
                min_dist = d
                closest_pt = (wp[0], wp[1])

        return closest_pt[0], closest_pt[1], round(min_dist, 1)

    @staticmethod
    def distance_meters(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Haversine distance in meters."""
        d_lat = math.radians(lat2 - lat1)
        d_lng = math.radians(lng2 - lng1)
        a = (math.sin(d_lat / 2.0) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(d_lng / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return DeadReckoningEngine.EARTH_RADIUS_KM * 1000.0 * c
