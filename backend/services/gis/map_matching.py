"""
CityBus Enterprise Platform - GPS Map-Matching & Road Snapping Engine
File: backend/services/gis/map_matching.py

Snaps raw, noisy GPS telemetry coordinates to route corridor polylines:
- Orthogonal projection onto polyline line segments
- Emission and transition probability scoring
- Off-route detection with threshold alerts
"""

import math
from typing import List, Tuple, Dict, Any, Optional


class MapMatchingEngine:
    """Snaps noisy GPS points to route geometry."""

    @staticmethod
    def project_point_to_segment(p: Tuple[float, float], a: Tuple[float, float], b: Tuple[float, float]) -> Tuple[float, float, float]:
        """
        Projects point P(lat, lng) onto line segment AB.
        Returns (projected_lat, projected_lng, distance_meters).
        """
        lat, lng = p
        lat_a, lng_a = a
        lat_b, lng_b = b

        # Vector AB
        d_lat = lat_b - lat_a
        d_lng = lng_b - lng_a

        if d_lat == 0 and d_lng == 0:
            # Segment is a point
            dist = MapMatchingEngine.haversine_m(lat, lng, lat_a, lng_a)
            return (lat_a, lng_a, dist)

        # Projection parameter t = ((P - A) . (B - A)) / |AB|^2
        t = ((lat - lat_a) * d_lat + (lng - lng_a) * d_lng) / (d_lat * d_lat + d_lng * d_lng)
        t = max(0.0, min(1.0, t)) # Clamp to segment bounds

        proj_lat = lat_a + t * d_lat
        proj_lng = lng_a + t * d_lng
        dist = MapMatchingEngine.haversine_m(lat, lng, proj_lat, proj_lng)

        return (proj_lat, proj_lng, dist)

    @staticmethod
    def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371008.8
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lam = math.radians(lon2 - lon1)
        a = (math.sin(d_phi / 2.0) ** 2 +
             math.cos(phi1) * math.cos(phi2) *
             math.sin(d_lam / 2.0) ** 2)
        return R * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    @staticmethod
    def match_to_polyline(gps_lat: float, gps_lng: float, polyline: List[Tuple[float, float]], max_snap_distance_m: float = 60.0) -> Dict[str, Any]:
        """
        Snaps a raw GPS ping to the nearest polyline segment.
        """
        if not polyline or len(polyline) < 2:
            return {
                'snapped_lat': gps_lat,
                'snapped_lng': gps_lng,
                'distance_to_route_m': 0.0,
                'is_on_route': True,
                'segment_index': 0
            }

        p = (float(gps_lat), float(gps_lng))
        best_proj = None
        min_dist = float('inf')
        best_segment_idx = 0

        for i in range(len(polyline) - 1):
            a = polyline[i]
            b = polyline[i + 1]
            proj_lat, proj_lng, dist = MapMatchingEngine.project_point_to_segment(p, a, b)

            if dist < min_dist:
                min_dist = dist
                best_proj = (proj_lat, proj_lng)
                best_segment_idx = i

        is_on_route = min_dist <= max_snap_distance_m

        return {
            'snapped_lat': round(best_proj[0], 6) if best_proj else gps_lat,
            'snapped_lng': round(best_proj[1], 6) if best_proj else gps_lng,
            'distance_to_route_m': round(min_dist, 2),
            'is_on_route': is_on_route,
            'segment_index': best_segment_idx
        }
