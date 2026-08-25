"""
CityBus Enterprise Platform - Deadheading Distance & Fuel Cost Calculator
File: backend/services/scheduling/deadhead_calculator.py

Calculates non-revenue positioning miles between depots and route terminals:
- Distance matrix between depots (PNBS Depot, Autonagar Depot, Mangalagiri Depot, Gannavaram Depot)
- Travel time estimations by time of day
- Diesel (L) and EV electricity (kWh) consumption cost calculations
"""

from typing import Dict, Tuple


class DeadheadCalculator:
    DEPOT_COORDINATES = {
        'PNBS_CENTRAL': (16.5100, 80.6175),
        'AUTONAGAR_DEPOT': (16.4950, 80.6780),
        'MANGALAGIRI_DEPOT': (16.4350, 80.5700),
        'GANNAVARAM_DEPOT': (16.5400, 80.7950)
    }

    FUEL_COST_PER_LITER = 94.50
    EV_RATE_PER_KWH = 7.20
    DIESEL_KM_PER_LITER = 3.8
    EV_KWH_PER_KM = 1.15

    @staticmethod
    def calculate_cost(distance_km: float, is_electric: bool = False) -> Dict[str, float]:
        """
        Calculates deadhead fuel or energy cost for a non-revenue positioning move.
        """
        if is_electric:
            kwh_used = distance_km * DeadheadCalculator.EV_KWH_PER_KM
            cost = kwh_used * DeadheadCalculator.EV_RATE_PER_KWH
            return {
                'distance_km': round(distance_km, 2),
                'energy_used_kwh': round(kwh_used, 2),
                'cost_inr': round(cost, 2),
                'powertrain': 'ELECTRIC'
            }
        else:
            liters_used = distance_km / DeadheadCalculator.DIESEL_KM_PER_LITER
            cost = liters_used * DeadheadCalculator.FUEL_COST_PER_LITER
            return {
                'distance_km': round(distance_km, 2),
                'fuel_used_liters': round(liters_used, 2),
                'cost_inr': round(cost, 2),
                'powertrain': 'DIESEL'
            }
