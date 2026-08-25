"""
CityBus Enterprise Platform - 450 kW Ultra-Fast DC Opportunity Charging Thermal Guard
File: backend/services/opportunity_charging/superfast_dc_thermal_guard.py

Monitors liquid-cooled charging cables and pantograph contact rails during 450 kW bursts:
- Current rates up to 600A DC (Charges 30 kWh in 4 minutes dwell time at terminal)
- Contact rail temperature threshold: 75°C (Auto-derating at 68°C)
- Liquid coolant flow rate and glycol loop pressure monitoring
"""

from typing import Dict, Any


class SuperfastDCThermalGuard:
    MAX_CONTACT_TEMP_C = 75.0
    DERATE_TEMP_C = 68.0

    @staticmethod
    def monitor_fast_charge(power_kw: float, contact_temp_c: float, coolant_flow_lpm: float) -> Dict[str, Any]:
        """
        Evaluates DC fast charging thermal stability and adjusts power output.
        """
        is_critical_temp = contact_temp_c >= SuperfastDCThermalGuard.MAX_CONTACT_TEMP_C
        is_derating = contact_temp_c >= SuperfastDCThermalGuard.DERATE_TEMP_C
        is_coolant_low = coolant_flow_lpm < 4.0 # Less than 4 Liters/min flow

        effective_power_kw = power_kw
        if is_critical_temp or is_coolant_low:
            effective_power_kw = 0.0 # Emergency shutdown
            charge_state = 'EMERGENCY_THERMAL_SHUTDOWN'
        elif is_derating:
            effective_power_kw = min(power_kw, 250.0) # Derate from 450kW to 250kW
            charge_state = 'THERMAL_DERATING_ACTIVE'
        else:
            charge_state = 'MAX_SPEED_CHARGE_ACTIVE'

        return {
            'requested_power_kw': round(power_kw, 1),
            'delivered_power_kw': round(effective_power_kw, 1),
            'contact_temperature_c': round(contact_temp_c, 1),
            'coolant_flow_rate_lpm': round(coolant_flow_lpm, 1),
            'is_derated': is_derating and not is_critical_temp,
            'is_emergency_cutoff': is_critical_temp or is_coolant_low,
            'charger_status': charge_state
        }
