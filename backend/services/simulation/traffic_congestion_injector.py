"""
CityBus Enterprise Platform - Dynamic Traffic Congestion & Bottleneck Injector
File: backend/services/simulation/traffic_congestion_injector.py

Injects dynamic traffic velocity changes into simulation corridors:
- SEVERE_CONGESTION (Speeds drop to 8-12 km/h)
- MODERATE_TRAFFIC (Speeds drop to 20-25 km/h)
- FREE_FLOW (Speeds nominal 35-48 km/h)
"""

from typing import Dict, Any, List


class CongestionInjector:
    CONGESTION_ZONES = {
        'BENZ_CIRCLE_FLYOVER': {'lat': 16.5020, 'lng': 80.6475, 'radius_km': 1.2, 'speed_reduction_pct': 0.65},
        'PRAKASHAM_BARRAGE': {'lat': 16.5070, 'lng': 80.6140, 'radius_km': 0.8, 'speed_reduction_pct': 0.80},
        'RAMAVARAPPADU_RING': {'lat': 16.5180, 'lng': 80.6720, 'radius_km': 1.0, 'speed_reduction_pct': 0.45}
    }

    @staticmethod
    def adjust_speed_for_congestion(lat: float, lng: float, nominal_speed_kmh: float) -> float:
        """
        Adjusts nominal speed based on active congestion hotspots.
        """
        for zone_name, zone in CongestionInjector.CONGESTION_ZONES.items():
            d_lat = lat - zone['lat']
            d_lng = lng - zone['lng']
            dist_km = (d_lat*d_lat + d_lng*d_lng) ** 0.5 * 111.0

            if dist_km <= zone['radius_km']:
                reduced_speed = nominal_speed_kmh * (1.0 - zone['speed_reduction_pct'])
                return max(6.0, round(reduced_speed, 1))

        return nominal_speed_kmh
