"""
CityBus Enterprise Platform - Demographic Concession & Off-Peak Discount Engine
File: backend/services/fare_capping/off_peak_concession_evaluator.py

Evaluates statutory concession entitlements and time-of-day discounts:
- SENIOR_CITIZEN (60+ years): 50% discount
- STUDENT_PASS_HOLDER: 60% discount
- OFF_PEAK_MIDDAY (11:00 to 15:30): 25% discount to flatten commuter peak curves
"""

from typing import Dict, Any


class ConcessionFareEvaluator:
    CONCESSION_RATES = {
        'SENIOR_CITIZEN': 0.50, # 50% discount
        'STUDENT': 0.60,        # 60% discount
        'DISABLED_PERSON': 1.0, # 100% free
        'GENERAL': 0.0
    }

    @staticmethod
    def calculate_concession_fare(base_fare_inr: float,
                                  passenger_category: str,
                                  is_off_peak_hours: bool = False) -> Dict[str, Any]:
        """
        Computes final ticket fare after concessions and off-peak incentives.
        """
        cat = passenger_category.upper().strip()
        discount_rate = ConcessionFareEvaluator.CONCESSION_RATES.get(cat, 0.0)

        # Off-peak additional 25% discount for general passengers
        if is_off_peak_hours and discount_rate == 0.0:
            discount_rate = 0.25
            discount_name = 'OFF_PEAK_MIDDAY_25PCT'
        else:
            discount_name = cat

        discount_amount = base_fare_inr * discount_rate
        final_fare = max(0.0, base_fare_inr - discount_amount)

        return {
            'base_fare_inr': round(base_fare_inr, 2),
            'applied_concession': discount_name,
            'discount_percentage': round(discount_rate * 100.0, 1),
            'discount_amount_inr': round(discount_amount, 2),
            'final_payable_fare_inr': round(final_fare, 2),
            'is_concession_applied': discount_rate > 0.0
        }
