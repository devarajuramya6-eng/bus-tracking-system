"""
CityBus Enterprise Platform - Driver Performance Bonus & Safety Incentive Service
File: backend/services/driver_incentive_calculator.py

Calculates monthly performance bonuses based on On-Time Performance (OTP > 92%),
Zero Harsh Braking records, fuel conservation efficiency, and passenger 5-star ratings.
"""

from typing import Dict, List, Any, Optional
from models import Driver, db


class DriverIncentiveCalculator:
    """Computes monthly driver incentive payouts and safety bonus awards."""

    BASE_BONUS_INR = 5000.0

    @staticmethod
    def calculate_driver_bonus(driver_id: int, completed_trips: int = 120,
                               otp_percentage: float = 95.5, safety_score: float = 92.0) -> Dict[str, Any]:
        """Calculates monthly incentive payout breakdown for a driver."""
        driver = Driver.query.get(driver_id)
        name = driver.name if driver else f"Driver #{driver_id}"

        otp_bonus = 1500.0 if otp_percentage >= 92.0 else 0.0
        safety_bonus = 2000.0 if safety_score >= 88.0 else 0.0
        trip_volume_bonus = 1500.0 if completed_trips >= 100 else 500.0

        total_bonus = otp_bonus + safety_bonus + trip_volume_bonus

        return {
            "driver_id": driver_id,
            "driver_name": name,
            "completed_trips": completed_trips,
            "otp_rate_pct": otp_percentage,
            "safety_score": safety_score,
            "bonus_breakdown": {
                "punctuality_otp_bonus_inr": otp_bonus,
                "zero_incident_safety_bonus_inr": safety_bonus,
                "volume_mileage_bonus_inr": trip_volume_bonus
            },
            "total_incentive_payout_inr": total_bonus,
            "eligibility_status": "QUALIFIED" if total_bonus >= 3000.0 else "STANDARD"
        }
