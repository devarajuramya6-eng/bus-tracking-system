"""
CityBus Enterprise Platform - EV Traction Battery Glycol Chiller Loop Controller
File: backend/services/thermal_inverter/battery_glycol_chiller_loop.py

Maintains 800V lithium-ion battery pack within optimal 22°C - 32°C envelope:
- Controls 50/50 Water-Ethylene Glycol auxiliary chiller plate loop
- Modulates variable speed 24V BLDC glycol pump (10 to 45 Liters/min)
- Active refrigerant plate chiller engages when pack temperature exceeds 33.0°C
"""

from typing import Dict, Any


class BatteryGlycolChillerLoop:
    OPTIMAL_MIN_TEMP_C = 22.0
    OPTIMAL_MAX_TEMP_C = 32.0
    CHILLER_ENGAGE_TEMP_C = 33.0

    @staticmethod
    def regulate_battery_thermal_loop(avg_battery_cell_temp_c: float,
                                      ambient_temp_c: float) -> Dict[str, Any]:
        """
        Calculates required glycol pump flow rate and chiller state.
        """
        if avg_battery_cell_temp_c >= BatteryGlycolChillerLoop.CHILLER_ENGAGE_TEMP_C:
            pump_flow_lpm = 42.0 # Max flow
            chiller_active = True
            loop_mode = 'ACTIVE_REFRIGERANT_CHILLER_COOLING'
        elif avg_battery_cell_temp_c > BatteryGlycolChillerLoop.OPTIMAL_MAX_TEMP_C:
            pump_flow_lpm = 25.0
            chiller_active = False # Passive radiator cooling
            loop_mode = 'PASSIVE_RADIATOR_CIRCULATION'
        elif avg_battery_cell_temp_c < BatteryGlycolChillerLoop.OPTIMAL_MIN_TEMP_C:
            pump_flow_lpm = 15.0
            chiller_active = False
            loop_mode = 'BATTERY_PTC_HEATER_PREWARMING'
        else:
            pump_flow_lpm = 12.0
            chiller_active = False
            loop_mode = 'STANDBY_TRICKLE_CIRCULATION'

        return {
            'avg_battery_cell_temp_c': round(avg_battery_cell_temp_c, 1),
            'ambient_temperature_c': round(ambient_temp_c, 1),
            'glycol_pump_flow_lpm': pump_flow_lpm,
            'is_refrigerant_chiller_active': chiller_active,
            'thermal_regulation_mode': loop_mode,
            'is_within_optimal_lifespan_window': BatteryGlycolChillerLoop.OPTIMAL_MIN_TEMP_C <= avg_battery_cell_temp_c <= BatteryGlycolChillerLoop.OPTIMAL_MAX_TEMP_C
        }
