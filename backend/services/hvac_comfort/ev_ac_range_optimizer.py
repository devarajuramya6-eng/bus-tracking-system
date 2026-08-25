"""
CityBus Enterprise Platform - EV HVAC Power Throttling & Range Preserver
File: backend/services/hvac_comfort/ev_ac_range_optimizer.py

Manages HVAC auxiliary electric power draw to preserve EV driving range:
- Heavy AC cooling can consume 12-18 kW on 45°C hot summer days in Vijayawada
- If Battery SoC < 25%, throttles HVAC to Eco-Pulse mode to guarantee bus reaches depot
"""

from typing import Dict, Any


class EVHVACRangeOptimizer:
    @staticmethod
    def optimize_hvac_draw(battery_soc_pct: float, ambient_temp_c: float,
                           remaining_route_distance_km: float,
                           estimated_driving_range_km: float) -> Dict[str, Any]:
        """
        Calculates maximum allowable HVAC kW power to avoid stranding.
        """
        range_margin_km = estimated_driving_range_km - remaining_route_distance_km

        if battery_soc_pct <= 18.0 or range_margin_km < 8.0:
            hvac_mode = 'EMERGENCY_ECO_THROTTLE'
            max_hvac_kw = 4.5
            cabin_setpoint_c = 26.5
        elif battery_soc_pct <= 30.0 or range_margin_km < 15.0:
            hvac_mode = 'BALANCED_RANGE_PRESERVATION'
            max_hvac_kw = 8.0
            cabin_setpoint_c = 25.0
        else:
            hvac_mode = 'MAX_COMFORT_COOLING'
            max_hvac_kw = 16.0
            cabin_setpoint_c = 23.0

        return {
            'battery_soc_pct': round(battery_soc_pct, 1),
            'ambient_temperature_c': round(ambient_temp_c, 1),
            'range_margin_km': round(range_margin_km, 1),
            'hvac_operating_mode': hvac_mode,
            'max_allowable_hvac_kw': max_hvac_kw,
            'target_setpoint_celsius': cabin_setpoint_c,
            'range_preserved_bonus_km': round((16.0 - max_hvac_kw) * 0.8, 1)
        }
