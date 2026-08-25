"""
CityBus Enterprise Platform - AI Defensive Driving Personalized Coaching Engine
File: backend/services/driver_training/defensive_driving_recommender.py

Generates personalized micro-learning modules based on driver infractions:
- Harsh Braking ➔ 3-Second Following Distance & Predictive Stopping module
- High-G Turns ➔ Low-Floor Passenger Standee Centrifugal Stability module
- Tailgating ➔ Hazard Anticipation & Brake Pre-Charging module
"""

from typing import List, Dict, Any


class DefensiveDrivingCoachingEngine:
    COACHING_MODULES = {
        'HARSH_BRAKING': {
            'module_id': 'MOD_SAFE_STOP',
            'title': 'Predictive Deceleration & 3-Second Following Distance',
            'duration_min': 8,
            'summary': 'Anticipate traffic signals 100 meters ahead to execute progressive smooth brake applications.'
        },
        'HARSH_TURNING': {
            'module_id': 'MOD_CORNER_G',
            'title': 'Centrifugal Passenger Standee Stability in Urban Roundabouts',
            'duration_min': 6,
            'summary': 'Slow down to < 18 km/h before entering Benz Circle roundabout to prevent standing passenger falls.'
        },
        'OVERSPEEDING': {
            'module_id': 'MOD_SPEED_ZONE',
            'title': 'Urban Arterial Speed Zoning & Pedestrian Safety',
            'duration_min': 10,
            'summary': 'Adhere strictly to 40 km/h municipal corridor limit. Speeding increases stopping distance quadratically.'
        }
    }

    @staticmethod
    def recommend_training(harsh_brakes: int, harsh_turns: int, overspeed_count: int) -> List[Dict[str, Any]]:
        """
        Assigns personalized training modules based on infractions.
        """
        assigned = []
        if harsh_brakes >= 2:
            assigned.append(DefensiveDrivingCoachingEngine.COACHING_MODULES['HARSH_BRAKING'])
        if harsh_turns >= 2:
            assigned.append(DefensiveDrivingCoachingEngine.COACHING_MODULES['HARSH_TURNING'])
        if overspeed_count >= 1:
            assigned.append(DefensiveDrivingCoachingEngine.COACHING_MODULES['OVERSPEEDING'])

        return assigned
