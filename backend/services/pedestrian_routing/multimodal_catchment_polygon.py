"""
CityBus Enterprise Platform - Pedestrian Walkshed Catchment Polygon Generator
File: backend/services/pedestrian_routing/multimodal_catchment_polygon.py

Computes first-mile / last-mile 400m and 800m walkshed polygons around transit stops:
- 5-Minute walk boundary (400 meters)
- 10-Minute walk boundary (800 meters)
- Estimates total residential catchment population served
"""

import math
from typing import List, Dict, Any


class CatchmentPolygonGenerator:
    WALKING_SPEED_METERS_PER_MIN = 75.0 # ~4.5 km/h

    @staticmethod
    def generate_walkshed_geometry(center_lat: float, center_lng: float, walk_minutes: List[int] = None) -> Dict[str, Any]:
        """
        Builds concentric pedestrian walkshed contours.
        """
        walk_times = walk_minutes or [5, 10]
        polygons = []

        for t_min in walk_times:
            radius_m = t_min * CatchmentPolygonGenerator.WALKING_SPEED_METERS_PER_MIN
            radius_km = radius_m / 1000.0

            # 16-point circle approximation
            coords = []
            for i in range(16):
                angle = (2.0 * math.pi * i) / 16.0
                d_lat = (radius_km / 111.0) * math.cos(angle)
                d_lng = (radius_km / (111.0 * math.cos(math.radians(center_lat)))) * math.sin(angle)
                coords.append([round(center_lat + d_lat, 6), round(center_lng + d_lng, 6)])
            coords.append(coords[0])

            # Population served estimation (approx 8,500 people per sq km in urban Vijayawada)
            area_sq_km = math.pi * (radius_km ** 2)
            est_population = int(area_sq_km * 8500)

            polygons.append({
                'walk_time_minutes': t_min,
                'radius_meters': int(radius_m),
                'estimated_population_served': est_population,
                'polygon': coords,
                'fill_color': '#10B981' if t_min <= 5 else '#3B82F6'
            })

        return {
            'center': [center_lat, center_lng],
            'walksheds': polygons
        }
