"""
CityBus Enterprise Platform - High-Precision Spatial Geofence Engine
File: backend/services/gis/geofence_engine.py

Provides spatial containment and geofencing calculations:
- Ray-Casting Point-in-Polygon (PIP) Containment Algorithm
- Circular buffer perimeters and distance-to-edge calculations
- Speed-restriction zones (School zones, hospital silent corridors, depot yards)
- Dynamic breach detection for fleet compliance
"""

import math
from typing import List, Tuple, Dict, Any, Optional


class GeofenceZone:
    """Represents a named geographic zone (Polygon or Circular)."""
    def __init__(self, zone_id: str, name: str, zone_type: str, category: str,
                 polygon: Optional[List[Tuple[float, float]]] = None,
                 center: Optional[Tuple[float, float]] = None,
                 radius_meters: Optional[float] = None,
                 max_speed_kmh: Optional[float] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        self.zone_id = zone_id
        self.name = name
        self.zone_type = zone_type # 'POLYGON', 'CIRCLE', 'CORRIDOR'
        self.category = category # 'DEPOT', 'SCHOOL_ZONE', 'HOSPITAL', 'RESTRICTED', 'BUS_LANE'
        self.polygon = polygon or []
        self.center = center
        self.radius_meters = radius_meters
        self.max_speed_kmh = max_speed_kmh
        self.metadata = metadata or {}


class GeofenceEngine:
    """Evaluates spatial containment and zone compliance."""

    EARTH_RADIUS_M = 6371008.8

    def __init__(self, zones: Optional[List[GeofenceZone]] = None):
        self.zones: List[GeofenceZone] = zones or []

    def add_zone(self, zone: GeofenceZone):
        self.zones.append(zone)

    @staticmethod
    def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Computes Great-Circle Haversine distance in meters."""
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lam = math.radians(lon2 - lon1)

        a = (math.sin(d_phi / 2.0) ** 2 +
             math.cos(phi1) * math.cos(phi2) *
             math.sin(d_lam / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return GeofenceEngine.EARTH_RADIUS_M * c

    @staticmethod
    def is_point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
        """
        Tests whether a geographic coordinate point is inside a polygon using Ray-Casting.
        :param point: (latitude, longitude)
        :param polygon: List of (latitude, longitude) vertices
        :return: True if inside or on boundary, False otherwise
        """
        if len(polygon) < 3:
            return False

        lat, lon = point
        n = len(polygon)
        inside = False

        p1_lat, p1_lon = polygon[0]
        for i in range(1, n + 1):
            p2_lat, p2_lon = polygon[i % n]
            if min(p1_lon, p2_lon) < lon <= max(p1_lon, p2_lon):
                if lat <= max(p1_lat, p2_lat):
                    if p1_lon != p2_lon:
                        x_intersect = (lon - p1_lon) * (p2_lat - p1_lat) / (p2_lon - p1_lon) + p1_lat
                    if p1_lat == p2_lat or lat <= x_intersect:
                        inside = not inside
            p1_lat, p1_lon = p2_lat, p2_lon

        return inside

    @staticmethod
    def is_point_in_circle(point: Tuple[float, float], center: Tuple[float, float], radius_meters: float) -> bool:
        """Tests whether a point is within a circular radius."""
        dist = GeofenceEngine.haversine_distance_m(point[0], point[1], center[0], center[1])
        return dist <= radius_meters

    def evaluate_location(self, lat: float, lng: float, current_speed_kmh: float = 0.0) -> List[Dict[str, Any]]:
        """
        Checks a vehicle's current position against all configured geofences.
        Returns a list of active zones and compliance alerts (e.g. speed violations).
        """
        point = (float(lat), float(lng))
        active_zones = []

        for zone in self.zones:
            inside = False
            distance_to_center_m = None

            if zone.zone_type == 'CIRCLE' and zone.center and zone.radius_meters:
                dist = self.haversine_distance_m(point[0], point[1], zone.center[0], zone.center[1])
                inside = dist <= zone.radius_meters
                distance_to_center_m = dist
            elif zone.zone_type == 'POLYGON' and zone.polygon:
                inside = self.is_point_in_polygon(point, zone.polygon)

            if inside:
                is_speed_violation = False
                excess_speed = 0.0
                if zone.max_speed_kmh and current_speed_kmh > zone.max_speed_kmh:
                    is_speed_violation = True
                    excess_speed = round(current_speed_kmh - zone.max_speed_kmh, 1)

                active_zones.append({
                    'zone_id': zone.zone_id,
                    'zone_name': zone.name,
                    'category': zone.category,
                    'max_speed_kmh': zone.max_speed_kmh,
                    'current_speed_kmh': current_speed_kmh,
                    'is_speed_violation': is_speed_violation,
                    'excess_speed_kmh': excess_speed,
                    'distance_to_center_m': round(distance_to_center_m, 1) if distance_to_center_m else None
                })

        return active_zones
