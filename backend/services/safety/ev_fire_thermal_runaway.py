"""
CityBus Enterprise Platform - EV High-Voltage Thermal Runaway & Fire Warning Engine
File: backend/services/safety/ev_fire_thermal_runaway.py

Monitors EV traction battery pack safety sensors (AIS-038 Rev 2):
- Cell Temperature Delta ($\Delta T > 8^\circ\text{C}$ between adjacent modules)
- Maximum Cell Temperature ($T > 62^\circ\text{C}$)
- Battery Enclosure Gas Sensor (CO and Hydrogen venting detection)
- Automated High Voltage (HV) Contactor and Pyrofuse trigger
"""

from typing import Dict, Any, List


class EVThermalRunawayMonitor:
    MAX_CELL_TEMP_CRITICAL_C = 62.0
    MAX_DELTA_TEMP_WARNING_C = 8.0

    @staticmethod
    def evaluate_pack_telemetry(bus_id: int,
                                max_cell_temp_c: float,
                                min_cell_temp_c: float,
                                gas_sensor_ppm: float,
                                insulation_resistance_kohm: float) -> Dict[str, Any]:
        """
        Evaluates battery pack thermal runaway risk.
        """
        delta_temp = max_cell_temp_c - min_cell_temp_c
        has_gas_venting = gas_sensor_ppm > 45.0
        is_low_insulation = insulation_resistance_kohm < 100.0 # Standard 500 kOhm

        is_critical = max_cell_temp_c >= EVThermalRunawayMonitor.MAX_CELL_TEMP_CRITICAL_C or (has_gas_venting and delta_temp >= 6.0)

        if is_critical:
            return {
                'bus_id': bus_id,
                'status': 'CRITICAL_THERMAL_RUNAWAY_TRIGGERED',
                'safety_action': 'EMERGENCY_HV_CONTACTOR_OPEN_AND_EVACUATE',
                'max_cell_temp_c': max_cell_temp_c,
                'delta_temp_c': round(delta_temp, 1),
                'gas_ppm': gas_sensor_ppm,
                'insulation_kohm': insulation_resistance_kohm,
                'cockpit_alarm': True,
                'hvac_smoke_purge': True,
                'doors_emergency_unlock': True,
                'message': f"CRITICAL: Battery Thermal Runaway risk on Bus {bus_id}! Cell Temp: {max_cell_temp_c}°C, Venting: {gas_sensor_ppm}ppm."
            }

        elif delta_temp >= EVThermalRunawayMonitor.MAX_DELTA_TEMP_WARNING_C or is_low_insulation:
            return {
                'bus_id': bus_id,
                'status': 'THERMAL_STRESS_WARNING',
                'safety_action': 'REDUCE_DRIVE_TORQUE_LIMIT_CURRENT',
                'max_cell_temp_c': max_cell_temp_c,
                'delta_temp_c': round(delta_temp, 1),
                'gas_ppm': gas_sensor_ppm,
                'insulation_kohm': insulation_resistance_kohm,
                'cockpit_alarm': False,
                'doors_emergency_unlock': False,
                'message': f"Warning: High battery cell temperature variance of {delta_temp:.1f}°C detected on Bus {bus_id}."
            }

        return {
            'bus_id': bus_id,
            'status': 'BATTERY_PACK_NOMINAL',
            'safety_action': 'NORMAL_OPERATION',
            'max_cell_temp_c': max_cell_temp_c,
            'delta_temp_c': round(delta_temp, 1),
            'gas_ppm': gas_sensor_ppm,
            'insulation_kohm': insulation_resistance_kohm
        }
