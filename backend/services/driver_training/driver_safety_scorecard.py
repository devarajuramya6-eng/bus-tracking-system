"""
CityBus Enterprise Platform - Driver Safety Telematics Scorecard (100-Point Model)
File: backend/services/driver_training/driver_safety_scorecard.py

Calculates comprehensive driver performance score (0 to 100):
- Deducts points for Harsh Braking events (-4 pts/event)
- Deducts points for Rapid Acceleration (-3 pts/event)
- Deducts points for Aggressive Cornering (-5 pts/event)
- Deducts points for Speeding Violations (-10 pts/event)
- Classifies driver into: MASTER_CAPTAIN (90+), SAFE_DRIVER (75-89), NEEDS_COACHING (< 75)
"""

from typing import Dict, Any


class DriverSafetyScorecardEngine:
    @staticmethod
    def compute_scorecard(driver_id: int, driver_name: str, distance_km: float,
                          harsh_brakes: int, rapid_accels: int,
                          harsh_turns: int, overspeed_events: int,
                          idle_minutes: float = 12.0) -> Dict[str, Any]:
        """
        Calculates driver index and safety tier.
        """
        base_score = 100.0

        # Normalized penalty per 100 km
        norm_factor = 100.0 / max(10.0, distance_km)

        penalty = (harsh_brakes * 4.0 + rapid_accels * 3.0 + harsh_turns * 5.0 + overspeed_events * 10.0) * norm_factor
        final_score = max(10.0, min(100.0, base_score - penalty))

        if final_score >= 90.0:
            tier = 'MASTER_CAPTAIN'
            incentive_bonus_inr = 500.0
        elif final_score >= 75.0:
            tier = 'SAFE_COMMERCIAL_DRIVER'
            incentive_bonus_inr = 200.0
        else:
            tier = 'MANDATORY_COACHING_REQUIRED'
            incentive_bonus_inr = 0.0

        return {
            'driver_id': driver_id,
            'driver_name': driver_name,
            'distance_evaluated_km': round(distance_km, 1),
            'safety_score': round(final_score, 1),
            'performance_tier': tier,
            'harsh_braking_count': harsh_brakes,
            'rapid_acceleration_count': rapid_accels,
            'harsh_cornering_count': harsh_turns,
            'overspeeding_violations': overspeed_events,
            'driver_safety_incentive_inr': incentive_bonus_inr
        }
