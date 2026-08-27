"""
CityBus Enterprise Platform - Turn-By-Turn Guidance Generator
File: backend/services/route_turn_by_turn_generator.py

Computes directional maneuvers, compass bearings, maneuver instructions,
and stop approach triggers for driver navigation HUDs.
"""

import math
from typing import List, Dict, Any, Tuple


class RouteTurnByTurnGenerator:
    """Generates sequential driving navigation steps from route waypoints and stops."""

    @staticmethod
    def generate_maneuvers(waypoints: List[List[float]], stops_sequence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transforms coordinate polyline into structured driver navigation instructions."""
        if not waypoints or len(waypoints) < 2:
            return []

        maneuvers = []
        # Step 1: Depart initial terminal
        first_pt = waypoints[0]
        second_pt = waypoints[1]
        initial_bearing = RouteTurnByTurnGenerator.calculate_bearing(first_pt[0], first_pt[1], second_pt[0], second_pt[1])

        start_name = stops_sequence[0].get('name', 'Terminal') if stops_sequence else "Terminal"
        maneuvers.append({
            "step": 1,
            "instruction": f"Depart from {start_name} heading {RouteTurnByTurnGenerator.bearing_to_compass(initial_bearing)}",
            "type": "DEPART",
            "bearing": round(initial_bearing, 1),
            "lat": first_pt[0],
            "lng": first_pt[1]
        })

        # Process intermediate waypoints
        for i in range(1, len(waypoints) - 1):
            prev_pt = waypoints[i - 1]
            curr_pt = waypoints[i]
            next_pt = waypoints[i + 1]

            b1 = RouteTurnByTurnGenerator.calculate_bearing(prev_pt[0], prev_pt[1], curr_pt[0], curr_pt[1])
            b2 = RouteTurnByTurnGenerator.calculate_bearing(curr_pt[0], curr_pt[1], next_pt[0], next_pt[1])

            angle_diff = (b2 - b1 + 180) % 360 - 180

            if abs(angle_diff) >= 30: # Significant turn
                turn_type = "TURN_RIGHT" if angle_diff > 0 else "TURN_LEFT"
                turn_dir = "right" if angle_diff > 0 else "left"
                maneuvers.append({
                    "step": len(maneuvers) + 1,
                    "instruction": f"Turn {turn_dir} at junction",
                    "type": turn_type,
                    "bearing": round(b2, 1),
                    "lat": curr_pt[0],
                    "lng": curr_pt[1]
                })

        # Add arrival maneuver
        last_pt = waypoints[-1]
        dest_name = stops_sequence[-1].get('name', 'Destination') if stops_sequence else "Destination"
        maneuvers.append({
            "step": len(maneuvers) + 1,
            "instruction": f"Arrive at destination: {dest_name}",
            "type": "ARRIVE",
            "bearing": 0.0,
            "lat": last_pt[0],
            "lng": last_pt[1]
        })

        return maneuvers

    @staticmethod
    def calculate_bearing(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculates compass heading from point 1 to point 2."""
        φ1 = math.radians(lat1)
        φ2 = math.radians(lat2)
        Δλ = math.radians(lng2 - lng1)
        y = math.sin(Δλ) * math.cos(φ2)
        x = math.cos(φ1) * math.sin(φ2) - math.sin(φ1) * math.cos(φ2) * math.cos(Δλ)
        θ = math.atan2(y, x)
        return (math.degrees(θ) + 360.0) % 360.0

    @staticmethod
    def bearing_to_compass(bearing: float) -> str:
        """Converts numerical bearing (0-360) into standard compass direction string."""
        compass_brackets = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
        idx = int((bearing + 22.5) / 45.0) % 8
        return compass_brackets[idx]
