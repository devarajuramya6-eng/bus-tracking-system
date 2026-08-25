"""
CityBus Enterprise Platform - Transit Corridor Spatial & Kinematic Analyzer
File: backend/services/gis/corridor_analyzer.py

Analyzes transit corridor characteristics:
- Angular road curvature and turning radius
- Cumulative elevation change and slope gradient
- Inter-stop segment runtime benchmarking
"""

import math
from typing import List, Tuple, Dict, Any


class CorridorAnalyzer:
    """Performs geometric and kinematic analysis on transit corridors."""

    @staticmethod
    def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculates forward initial compass bearing from Point 1 to Point 2 in degrees [0, 360)."""
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_lon = math.radians(lon2 - lon1)

        y = math.sin(delta_lon) * math.cos(phi2)
        x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lon)
        bearing = math.degrees(math.atan2(y, x))
        return (bearing + 360.0) % 360.0

    @staticmethod
    def calculate_turn_angles(waypoints: List[Tuple[float, float]]) -> List[Dict[str, Any]]:
        """
        Calculates deflection angles along a polyline to identify sharp turns and bottlenecks.
        """
        if len(waypoints) < 3:
            return []

        turns = []
        for i in range(len(waypoints) - 2):
            p1 = waypoints[i]
            p2 = waypoints[i + 1]
            p3 = waypoints[i + 2]

            b1 = CorridorAnalyzer.calculate_bearing(p1[0], p1[1], p2[0], p2[1])
            b2 = CorridorAnalyzer.calculate_bearing(p2[0], p2[1], p3[0], p3[1])

            diff = abs(b2 - b1)
            if diff > 180.0:
                diff = 360.0 - diff

            is_sharp = diff > 45.0

            turns.append({
                'vertex_index': i + 1,
                'coordinate': p2,
                'bearing_in': round(b1, 1),
                'bearing_out': round(b2, 1),
                'deflection_angle_deg': round(diff, 1),
                'is_sharp_turn': is_sharp,
                'recommended_speed_limit_kmh': 20.0 if is_sharp else 45.0
            })

        return turns
