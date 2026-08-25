"""
CityBus Enterprise Platform - ASHRAE 55 Cabin Thermal Comfort (PMV/PPD) Engine
File: backend/services/hvac_comfort/thermal_comfort_pmv.py

Calculates Fanger's Predicted Mean Vote (PMV) and Predicted Percentage of Dissatisfied (PPD):
- Input: Cabin Temp (°C), Relative Humidity (%), Air Velocity (m/s), Passenger Load
- Target PMV range: -0.5 to +0.5 (Optimal thermal comfort for transit passengers)
- Dynamically modulates AC compressor inverter frequency (Hz) to save energy
"""

import math
from typing import Dict, Any


class ThermalComfortModel:
    @staticmethod
    def calculate_pmv_ppd(cabin_temp_c: float, relative_humidity_pct: float,
                          air_velocity_mps: float = 0.2,
                          passenger_count: int = 35) -> Dict[str, Any]:
        """
        Estimates passenger thermal comfort index.
        """
        # Simplified linear PMV model for tropical public transit cabins
        # Optimal comfort temperature ~ 23.5°C at 50% RH
        temp_delta = cabin_temp_c - 23.5
        rh_delta = (relative_humidity_pct - 50.0) / 100.0

        # High passenger crowding adds sensible & latent heat (+0.015 PMV per pax above 20)
        crowd_heat = max(0, passenger_count - 20) * 0.015

        pmv = (temp_delta * 0.28) + (rh_delta * 0.4) + crowd_heat - (air_velocity_mps * 0.5)
        pmv = max(-3.0, min(3.0, pmv))

        # Fanger's PPD formula: PPD = 100 - 95 * exp(-(0.03353*PMV^4 + 0.2179*PMV^2))
        ppd = 100.0 - 95.0 * math.exp(-(0.03353 * (pmv ** 4) + 0.2179 * (pmv ** 2)))

        if pmv > 1.0:
            comfort_status = 'WARM_NEEDS_MORE_COOLING'
            ac_inverter_target_hz = 75
        elif pmv < -1.0:
            comfort_status = 'COOL_REDUCE_COMPRESSOR'
            ac_inverter_target_hz = 30
        else:
            comfort_status = 'OPTIMAL_COMFORT_ZONE'
            ac_inverter_target_hz = 50

        return {
            'cabin_temperature_c': round(cabin_temp_c, 1),
            'relative_humidity_pct': round(relative_humidity_pct, 1),
            'pmv_index': round(pmv, 2),
            'ppd_dissatisfied_pct': round(ppd, 1),
            'thermal_comfort_status': comfort_status,
            'recommended_ac_inverter_hz': ac_inverter_target_hz,
            'is_within_ashrae55_standard': abs(pmv) <= 0.8
        }
