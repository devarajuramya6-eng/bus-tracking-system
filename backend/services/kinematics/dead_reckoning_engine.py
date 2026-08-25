"""
CityBus Enterprise Platform - Odometry & Dead Reckoning Navigation Engine
File: backend/services/kinematics/dead_reckoning_engine.py

Propagates vehicle location during GPS signal blackouts:
- High-frequency wheel tick counter integration (e.g. 48 pulses per wheel revolution)
- Steering angle / Yaw rate curvature projection
- Geodesic position propagation on WGS-84 ellipsoid
"""

import math
from typing import Dict, Any, Tuple


class DeadReckoningEngine:
    WHEEL_CIRCUMFERENCE_METERS = 3.14159 * 1.05 # Approx 1.05m diameter commercial tire
    PULSES_PER_REV = 48
    EARTH_RADIUS_M = 6371008.8

    @staticmethod
    def propagate_position(start_lat: float, start_lng: float,
                           start_heading_deg: float,
                           wheel_pulses_delta: int,
                           yaw_rate_deg_per_sec: float,
                           dt_seconds: float) -> Dict[str, Any]:
        """
        Advances coordinate position using wheel odometry and gyro yaw rate.
        """
        # Distance traveled in meters
        revs = wheel_pulses_delta / float(DeadReckoningEngine.PULSES_PER_REV)
        dist_meters = revs * DeadReckoningEngine.WHEEL_CIRCUMFERENCE_METERS

        # New heading
        heading_delta = yaw_rate_deg_per_sec * dt_seconds
        new_heading_deg = (start_heading_deg + heading_delta + 360.0) % 360.0

        # Mean heading during time step
        mean_heading_rad = math.radians((start_heading_deg + (heading_delta / 2.0) + 360.0) % 360.0)

        # Geodesic delta
        d_north_m = dist_meters * math.cos(mean_heading_rad)
        d_east_m = dist_meters * math.sin(mean_heading_rad)

        delta_lat = (d_north_m / DeadReckoningEngine.EARTH_RADIUS_M) * (180.0 / math.pi)
        delta_lng = (d_east_m / (DeadReckoningEngine.EARTH_RADIUS_M * math.cos(math.radians(start_lat)))) * (180.0 / math.pi)

        new_lat = start_lat + delta_lat
        new_lng = start_lng + delta_lng

        speed_mps = dist_meters / max(0.001, dt_seconds)
        speed_kmh = speed_mps * 3.6

        return {
            'estimated_lat': round(new_lat, 6),
            'estimated_lng': round(new_lng, 6),
            'new_heading_deg': round(new_heading_deg, 1),
            'distance_traveled_m': round(dist_meters, 2),
            'speed_kmh': round(speed_kmh, 1),
            'navigation_mode': 'DEAD_RECKONING_ACTIVE'
        }
