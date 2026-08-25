"""
CityBus Enterprise Platform - Dynamic Daily & Weekly Fare Capping Engine
File: backend/services/fare_capping/daily_weekly_capping_engine.py

Implements automated best-value fare capping (TfL / OMNY standard):
- Daily Cap: ₹75.00 (Max single-day fare charged)
- Weekly Cap: ₹350.00 (Max 7-day rolling expenditure)
- Automatically grants ₹0.00 free rides once cap is reached
"""

from typing import Dict, Any


class FareCappingEngine:
    DAILY_CAP_INR = 75.0
    WEEKLY_CAP_INR = 350.0

    @staticmethod
    def calculate_capped_fare(standard_fare_inr: float,
                              accumulated_today_inr: float,
                              accumulated_week_inr: float) -> Dict[str, Any]:
        """
        Determines actual fare to debit after applying fare caps.
        """
        # Daily cap check
        daily_room = max(0.0, FareCappingEngine.DAILY_CAP_INR - accumulated_today_inr)
        weekly_room = max(0.0, FareCappingEngine.WEEKLY_CAP_INR - accumulated_week_inr)

        effective_room = min(daily_room, weekly_room)
        actual_debited_fare = min(standard_fare_inr, effective_room)
        savings_inr = max(0.0, standard_fare_inr - actual_debited_fare)

        is_daily_cap_reached = (accumulated_today_inr + actual_debited_fare) >= FareCappingEngine.DAILY_CAP_INR
        is_weekly_cap_reached = (accumulated_week_inr + actual_debited_fare) >= FareCappingEngine.WEEKLY_CAP_INR

        return {
            'standard_fare_inr': round(standard_fare_inr, 2),
            'actual_fare_debited_inr': round(actual_debited_fare, 2),
            'commuter_savings_inr': round(savings_inr, 2),
            'new_accumulated_today_inr': round(accumulated_today_inr + actual_debited_fare, 2),
            'new_accumulated_week_inr': round(accumulated_week_inr + actual_debited_fare, 2),
            'is_daily_capped': is_daily_cap_reached,
            'is_weekly_capped': is_weekly_cap_reached,
            'status': 'FREE_RIDE_FARE_CAPPED' if actual_debited_fare == 0.0 else 'PARTIALLY_CAPPED_OR_STANDARD'
        }
