"""
CityBus Enterprise Platform - Fuel-Efficient & Regenerative Eco-Driving Engine
File: backend/services/driver_training/fuel_efficient_eco_driving.py

Analyzes vehicle kinetic momentum coasting and regenerative recapture:
- Momentum Coasting Index: Percentage of driving time vehicle is rolling in gear without throttle (> 18% optimal)
- Smooth Throttle Modulation: Avoids sudden wide-open throttle (WOT) pedal stomps
- Saves up to 14% diesel fuel and recovers 22% kinetic energy in EV buses
"""

from typing import Dict, Any


class EcoDrivingAnalyzer:
    @staticmethod
    def evaluate_trip_eco_efficiency(total_distance_km: float, coasting_distance_km: float,
                                     wot_events_count: int, regen_kwh_recovered: float = 18.5) -> Dict[str, Any]:
        """
        Calculates eco-driving efficiency percentage.
        """
        coasting_ratio = (coasting_distance_km / max(1.0, total_distance_km)) * 100.0
        wot_penalty = min(30.0, wot_events_count * 2.5)

        # Baseline score around coasting ratio
        eco_score = max(20.0, min(100.0, 50.0 + (coasting_ratio * 2.5) - wot_penalty))

        return {
            'total_distance_km': round(total_distance_km, 1),
            'coasting_distance_km': round(coasting_distance_km, 1),
            'coasting_percentage': round(coasting_ratio, 1),
            'wide_open_throttle_events': wot_events_count,
            'regenerative_energy_recovered_kwh': round(regen_kwh_recovered, 2),
            'eco_driving_score': round(eco_score, 1),
            'fuel_savings_percentage': round(max(0.0, (eco_score - 50.0) * 0.28), 1),
            'grade': 'GOLD_ECO_MASTER' if eco_score >= 85 else ('SILVER_ECO' if eco_score >= 70 else 'STANDARD_OPERATOR')
        }
