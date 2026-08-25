"""
CityBus Enterprise Platform - Heat Pump 4-Way Valve & Waste Heat Reclaim
File: backend/services/thermal_inverter/refrigerant_flow_controller.py

Controls R1234yf / CO2 heat pump 4-way reversing valves on electric transit buses:
- SUMMER_COOLING: Evaporator in cabin ceiling vents / Condenser on roof
- WINTER_HEATING: Reverses refrigerant cycle to heat passenger cabin
- MOTOR_WASTE_HEAT_RECLAIM: Scavenges 8 kW of motor/inverter heat to warm cabin with COP > 3.4
"""

from typing import Dict, Any


class HeatPumpRefrigerantController:
    @staticmethod
    def select_heat_pump_mode(ambient_temp_c: float,
                              target_cabin_temp_c: float,
                              motor_coolant_temp_c: float) -> Dict[str, Any]:
        """
        Determines optimal valve positions and coefficient of performance (COP).
        """
        temp_diff = target_cabin_temp_c - ambient_temp_c

        if temp_diff > 3.0: # Cabin needs heating
            if motor_coolant_temp_c >= 45.0:
                mode = 'MOTOR_WASTE_HEAT_HARVESTING'
                cop = 3.6
                valve_state = 'HEAT_RECOVERY_EXCHANGER_OPEN'
            else:
                mode = 'HEAT_PUMP_HEATING_ACTIVE'
                cop = 2.8
                valve_state = 'FOUR_WAY_VALVE_REVERSED'
        else: # Cabin needs cooling
            mode = 'HEAT_PUMP_COOLING_ACTIVE'
            cop = 3.2
            valve_state = 'FOUR_WAY_VALVE_FORWARD'

        return {
            'ambient_temperature_c': round(ambient_temp_c, 1),
            'target_cabin_temperature_c': round(target_cabin_temp_c, 1),
            'motor_coolant_temperature_c': round(motor_coolant_temp_c, 1),
            'operating_mode': mode,
            'four_way_valve_state': valve_state,
            'estimated_cop': cop,
            'is_waste_heat_utilized': mode == 'MOTOR_WASTE_HEAT_HARVESTING'
        }
