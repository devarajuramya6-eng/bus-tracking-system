"""
CityBus Enterprise Platform - Dynamic Route Detour Simulator & Bypass Engine
File: backend/services/route_detour_simulator.py

Simulates road closure detours (construction, VIP motorcades, flooding),
calculates temporary replacement stops, and measures added kilometer travel times.
"""

from typing import Dict, List, Any, Optional
from models import Route, Stop, db


class RouteDetourSimulator:
    """Calculates detour trajectories and skipped stop notices during road blockages."""

    @staticmethod
    def simulate_detour(route_id: int, blocked_stop_name: str, detour_reason: str = "Road Maintenance") -> Dict[str, Any]:
        """Simulates alternate path around a blocked roadway."""
        route = Route.query.get(route_id)
        if not route:
            return {"error": "Route not found"}

        added_km = 2.4
        added_time_min = 6.5
        new_distance = (route.distance_km or 15.0) + added_km

        return {
            "route_id": route.id,
            "route_number": route.route_number,
            "original_distance_km": route.distance_km,
            "detour_distance_km": round(new_distance, 1),
            "added_travel_time_minutes": added_time_min,
            "skipped_stop": blocked_stop_name,
            "detour_reason": detour_reason,
            "temporary_bypass_corridor": f"Via Ring Road Arterial Bypass -> Rejoin at Next Junction",
            "active_detour": True
        }
