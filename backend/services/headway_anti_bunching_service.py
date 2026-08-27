"""
CityBus Enterprise Platform - Headway Regulation & Anti-Bunching Algorithm
File: backend/services/headway_anti_bunching_service.py

Implements automated speed adjustment recommendations to eliminate bus bunching:
- Dynamically holds leading vehicles at major stops
- Grants green-light TSP wave priority to lagging vehicles
- Stabilizes arterial corridor headway variance
"""

import math
from typing import Dict, List, Any, Optional
from models import Bus, Route, db


class HeadwayAntiBunchingService:
    """Calculates holding times and target cruising speeds to balance headway gaps."""

    @staticmethod
    def calculate_corridor_regulation(route_id: int, target_headway_sec: float = 480.0) -> List[Dict[str, Any]]:
        """Calculates anti-bunching control inputs for all active buses on a route."""
        buses = Bus.query.filter_by(route_id=route_id, status='On Route').all()
        if len(buses) < 2:
            return []

        controls = []
        for i in range(len(buses) - 1):
            leading = buses[i]
            trailing = buses[i + 1]

            # Simulated distance gap along route (meters)
            dist_meters = abs(leading.latitude - trailing.latitude) * 111000.0 + abs(leading.longitude - trailing.longitude) * 105000.0
            avg_speed_mps = max(5.0, (trailing.speed * 1000.0) / 3600.0)
            actual_headway_sec = dist_meters / avg_speed_mps

            deviation_sec = actual_headway_sec - target_headway_sec

            if deviation_sec < -120.0: # Bunching (< 6 min gap)
                action = "HOLD_LEADING_BUS"
                holding_time_sec = min(90, int(abs(deviation_sec) * 0.4))
                target_speed_trailing = 30.0 # Slow down trailing
            elif deviation_sec > 180.0: # Excessive gap (> 11 min gap)
                action = "EXPEDITE_TRAILING_BUS"
                holding_time_sec = 0
                target_speed_trailing = 48.0 # Speed up trailing
            else:
                action = "MAINTAIN"
                holding_time_sec = 0
                target_speed_trailing = 40.0

            controls.append({
                "leading_bus_id": leading.id,
                "leading_bus_number": leading.bus_number,
                "trailing_bus_id": trailing.id,
                "trailing_bus_number": trailing.bus_number,
                "actual_headway_seconds": round(actual_headway_sec, 1),
                "target_headway_seconds": target_headway_sec,
                "action": action,
                "recommended_holding_seconds": holding_time_sec,
                "target_speed_kmh": target_speed_trailing
            })

        return controls
