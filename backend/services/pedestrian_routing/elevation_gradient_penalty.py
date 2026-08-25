"""
CityBus Enterprise Platform - Tobler's Elevation & Slope Walking Penalty
File: backend/services/pedestrian_routing/elevation_gradient_penalty.py

Calculates pedestrian walking speed adjustment on slopes using Tobler's Hiking Function:
- Speed W = 6.0 * exp(-3.5 * |slope + 0.05|) km/h
- Steep uphill gradients (> 8% slope) significantly increase walking travel time
- Flags steps / hill stairways unsuitable for wheelchair or elderly commuters
"""

import math
from typing import Dict, Any


class ElevationWalkingPenalty:
    @staticmethod
    def calculate_slope_walking_speed(distance_m: float, elevation_gain_m: float) -> Dict[str, Any]:
        """
        Calculates terrain-adjusted walking speed and time.
        """
        slope = elevation_gain_m / max(1.0, distance_m)
        
        # Tobler's hiking formula in km/h
        speed_kmh = 6.0 * math.exp(-3.5 * abs(slope + 0.05))
        speed_kmh = max(1.2, min(5.5, speed_kmh)) # Clamp

        speed_mps = (speed_kmh * 1000.0) / 3600.0
        travel_time_sec = distance_m / speed_mps

        is_steep = slope >= 0.08
        is_wheelchair_inaccessible = slope >= 0.083 # > 1:12 ADA ramp limit

        return {
            'distance_meters': round(distance_m, 1),
            'elevation_gain_meters': round(elevation_gain_m, 1),
            'slope_gradient_pct': round(slope * 100.0, 1),
            'adjusted_walking_speed_kmh': round(speed_kmh, 2),
            'walking_time_seconds': int(round(travel_time_sec)),
            'is_steep_incline': is_steep,
            'is_ada_accessible': not is_wheelchair_inaccessible
        }
