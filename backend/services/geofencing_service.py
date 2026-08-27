"""
CityBus Enterprise Platform - Geofencing & Spatial Boundary Service
File: backend/services/geofencing_service.py

Monitors bus proximity to designated stop zones, terminal yards, depot geofences,
and detects route deviation violations in real time.
"""

import math
from typing import Dict, List, Any, Optional, Tuple
from models import Bus, Stop, Route, RouteStop, db


class GeofencingService:
    """Evaluates spatial relationships and geofence triggers for operating buses."""

    EARTH_RADIUS_METERS = 6371000.0

    @staticmethod
    def calculate_distance_meters(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculates exact Haversine distance in meters between two GPS coordinates."""
        d_lat = math.radians(lat2 - lat1)
        d_lng = math.radians(lng2 - lng1)
        a = (math.sin(d_lat / 2.0) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(d_lng / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return GeofencingService.EARTH_RADIUS_METERS * c

    @staticmethod
    def check_stop_geofences(bus_lat: float, bus_lng: float, route_id: Optional[int] = None, radius_meters: float = 80.0) -> List[Dict[str, Any]]:
        """Checks if a bus coordinate is inside any stop geofence along its route."""
        if route_id:
            route_stops = RouteStop.query.filter_by(route_id=route_id).order_by(RouteStop.stop_order.asc()).all()
            stops = [rs.stop for rs in route_stops if rs.stop]
        else:
            stops = Stop.query.all()

        triggered_stops = []
        for stop in stops:
            dist = GeofencingService.calculate_distance_meters(bus_lat, bus_lng, stop.latitude, stop.longitude)
            if dist <= radius_meters:
                triggered_stops.append({
                    "stop_id": stop.id,
                    "stop_name": stop.name,
                    "stop_code": stop.stop_code,
                    "distance_meters": round(dist, 1),
                    "is_inside": True
                })

        return triggered_stops

    @staticmethod
    def detect_route_deviation(bus_lat: float, bus_lng: float, route_id: int, max_corridor_drift_meters: float = 300.0) -> Tuple[bool, float]:
        """
        Determines if the vehicle has deviated significantly from its assigned route polyline.
        Returns (is_deviated, min_distance_to_corridor_meters).
        """
        route = Route.query.get(route_id)
        if not route:
            return False, 0.0

        waypoints = route.get_waypoints()
        if not waypoints:
            return False, 0.0

        # Find minimum distance to any route waypoint
        min_dist = float('inf')
        for wp in waypoints:
            dist = GeofencingService.calculate_distance_meters(bus_lat, bus_lng, wp[0], wp[1])
            if dist < min_dist:
                min_dist = dist

        is_deviated = min_dist > max_corridor_drift_meters
        return is_deviated, round(min_dist, 1)
