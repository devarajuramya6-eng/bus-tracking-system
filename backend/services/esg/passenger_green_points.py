"""
CityBus Enterprise Platform - Commuter Eco-Rewards & Green Carbon Points
File: backend/services/esg/passenger_green_points.py

Awards green points to passengers for choosing public transit over private vehicles:
- 10 Green Points awarded per kg of CO2 avoided
- Redeemable for ticket discounts, electric bus pass upgrades, and municipal partner rewards
"""

from typing import Dict, Any


class PassengerGreenPointsLedger:
    CO2_SAVED_PER_PASSENGER_KM_KG = 0.092 # Public bus vs private motorbike/car blend

    @staticmethod
    def award_trip_points(user_id: int, distance_km: float, is_electric_bus: bool = False) -> Dict[str, Any]:
        """
        Calculates eco points for a passenger trip.
        """
        co2_saved_kg = distance_km * PassengerGreenPointsLedger.CO2_SAVED_PER_PASSENGER_KM_KG
        if is_electric_bus:
            co2_saved_kg *= 1.35 # Extra bonus for zero-emission EV trips

        points_earned = int(round(co2_saved_kg * 10.0))
        points_earned = max(1, points_earned)

        return {
            'user_id': user_id,
            'distance_km': round(distance_km, 2),
            'is_electric_bus': is_electric_bus,
            'co2_avoided_kg': round(co2_saved_kg, 3),
            'green_points_earned': points_earned,
            'eco_badge_earned': 'ECO_WARRIOR' if points_earned >= 15 else 'GREEN_COMMUTER',
            'cash_value_rebate_inr': round(points_earned * 0.10, 2)
        }
