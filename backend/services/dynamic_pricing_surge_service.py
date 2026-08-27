"""
CityBus Enterprise Platform - Dynamic Surge Pricing & Elastic Demand Service
File: backend/services/dynamic_pricing_surge_service.py

Computes dynamic pricing multipliers for express transit lines during festival surges,
cricket matches at ACA-VDCA Stadium, and inclement monsoon downpours.
"""

from typing import Dict, List, Any, Optional


class DynamicPricingSurgeService:
    """Calculates time-of-day and weather-responsive dynamic fare multipliers."""

    SURGE_EVENTS = {
        "DIWALI_FESTIVAL_RUSH": {"multiplier": 1.25, "reason": "Diwali Festival Intercity Surge"},
        "MONSOON_HEAVY_RAIN":   {"multiplier": 1.15, "reason": "Severe Weather Surcharge & Road Drainage Detour"},
        "CRICKET_STADIUM_EVENT": {"multiplier": 1.30, "reason": "ACA Stadium Match Day Special Corridor"}
    }

    @classmethod
    def calculate_surge_fare(cls, base_fare: float, active_event_code: Optional[str] = None,
                             occupancy_pct: float = 50.0) -> Dict[str, Any]:
        """Calculates modified fare with applied surge constraints (capped at max 1.35x)."""
        multiplier = 1.0
        applied_reasons = []

        if active_event_code and active_event_code in cls.SURGE_EVENTS:
            evt = cls.SURGE_EVENTS[active_event_code]
            multiplier *= evt["multiplier"]
            applied_reasons.append(evt["reason"])

        # High occupancy pressure surcharge (>90% full)
        if occupancy_pct >= 90.0:
            multiplier *= 1.10
            applied_reasons.append("Peak Occupancy Demand (>90%)")

        capped_multiplier = min(1.35, multiplier)
        final_fare = round(base_fare * capped_multiplier, 2)

        return {
            "base_fare_inr": round(base_fare, 2),
            "surge_multiplier": round(capped_multiplier, 2),
            "surge_amount_inr": round(final_fare - base_fare, 2),
            "final_fare_inr": final_fare,
            "applied_factors": applied_reasons
        }
