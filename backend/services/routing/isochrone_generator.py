"""
CityBus Enterprise Platform - Transit Isochrone Catchment Contour Generator
File: backend/services/routing/isochrone_generator.py

Calculates travel-time reachability isochrones from transit stations:
- 15-minute, 30-minute, 45-minute, 60-minute reachability polygons
- First-mile pedestrian walking radius + bus in-vehicle travel speed
"""

import math
from typing import List, Dict, Any, Tuple


class IsochroneGenerator:
    """Generates geographic accessibility contours."""

    WALKING_SPEED_KMH = 4.5
    BUS_AVG_SPEED_KMH = 28.0

    @staticmethod
    def generate_isochrones(center_lat: float, center_lng: float, time_intervals_min: List[int] = None) -> Dict[str, Any]:
        """
        Computes concentric reachability contours.
        """
        intervals = time_intervals_min or [15, 30, 45, 60]
        contours = []

        for t_min in intervals:
            # Approx reachable radius in km (combination of transit + walk)
            reachable_km = (t_min / 60.0) * IsochroneGenerator.BUS_AVG_SPEED_KMH * 0.75

            # Generate circular polygon vertices
            polygon = []
            num_vertices = 16
            for i in range(num_vertices):
                angle_rad = (2.0 * math.pi * i) / num_vertices
                # Degree offset approximation
                d_lat = (reachable_km / 111.0) * math.cos(angle_rad)
                d_lng = (reachable_km / (111.0 * math.cos(math.radians(center_lat)))) * math.sin(angle_rad)
                polygon.append([round(center_lat + d_lat, 5), round(center_lng + d_lng, 5)])

            # Close polygon
            polygon.append(polygon[0])

            contours.append({
                'time_minutes': t_min,
                'radius_km': round(reachable_km, 2),
                'polygon_coordinates': polygon,
                'fill_color': '#10B981' if t_min <= 15 else ('#3B82F6' if t_min <= 30 else ('#F59E0B' if t_min <= 45 else '#EF4444'))
            })

        return {
            'center_coordinates': [center_lat, center_lng],
            'isochrones': contours
        }
