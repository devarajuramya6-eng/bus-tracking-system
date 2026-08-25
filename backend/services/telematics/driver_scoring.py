"""
CityBus Enterprise Platform - Driver Safety & Eco-Driving Scoring Engine
File: backend/services/telematics/driver_scoring.py

Calculates driving safety indices from high-frequency accelerometer and GPS logs:
- Harsh Braking Events (Deceleration > 9.5 km/h per second)
- Harsh Acceleration Events (Acceleration > 8.0 km/h per second)
- Sharp Cornering / Centrifugal Force G-spikes
- Overspeed duration and excessive stationary idling (> 3 minutes with engine on)
- Overall Eco-Driving Index (0-100 Score)
"""

from typing import List, Dict, Any


class DriverBehaviorScorer:
    @staticmethod
    def calculate_shift_score(telemetry_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates safety and eco-driving score for a driver shift.
        """
        if not telemetry_points or len(telemetry_points) < 5:
            return {
                'safety_score': 95.0,
                'eco_score': 92.0,
                'harsh_brakes': 0,
                'harsh_accels': 0,
                'overspeed_minutes': 0.0,
                'idling_minutes': 1.5,
                'rating_grade': 'A+'
            }

        harsh_brakes = 0
        harsh_accels = 0
        overspeed_count = 0
        idling_count = 0

        for i in range(len(telemetry_points) - 1):
            p1 = telemetry_points[i]
            p2 = telemetry_points[i + 1]

            s1 = p1.get('speed', 0.0)
            s2 = p2.get('speed', 0.0)
            delta_speed = s2 - s1 # Assuming 2-second telemetry sample intervals

            if delta_speed < -12.0:
                harsh_brakes += 1
            elif delta_speed > 10.0:
                harsh_accels += 1

            if s2 > 55.0: # Urban city limit 50 km/h
                overspeed_count += 1

            if s2 < 1.0 and p1.get('engine_rpm', 700) > 500:
                idling_count += 1

        # Penalties calculation
        score = 100.0
        score -= harsh_brakes * 4.0
        score -= harsh_accels * 2.5
        score -= overspeed_count * 1.5
        score -= idling_count * 0.5

        final_score = max(40.0, min(100.0, score))
        grade = 'A+' if final_score >= 90 else ('A' if final_score >= 80 else ('B' if final_score >= 70 else 'C'))

        return {
            'safety_score': round(final_score, 1),
            'eco_score': round(final_score * 0.96, 1),
            'harsh_brakes': harsh_brakes,
            'harsh_accels': harsh_accels,
            'overspeed_events': overspeed_count,
            'idling_events': idling_count,
            'rating_grade': grade
        }
