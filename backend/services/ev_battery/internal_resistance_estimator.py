"""
CityBus Enterprise Platform - Battery DC Internal Resistance (DCIR) Estimator
File: backend/services/ev_battery/internal_resistance_estimator.py

Estimates battery pack DC Internal Resistance (DCIR) during high-current pulses:
- Ohm's Law calculation: R_int = Delta V / Delta I during heavy regenerative braking / acceleration
- Tracks resistance growth over lifetime (R_int > 1.5x baseline indicates end-of-life battery degradation)
"""

from typing import Dict, Any


class BatteryInternalResistanceEstimator:
    BASELINE_DCIR_MOHM = 18.0 # Baseline milliohms when new
    MAX_ALLOWABLE_DCIR_MOHM = 32.0 # 1.77x baseline replacement threshold

    @staticmethod
    def estimate_dcir(voltage_before_pulse_v: float, voltage_during_pulse_v: float,
                      current_pulse_amperes: float) -> Dict[str, Any]:
        """
        Estimates pack internal resistance from load pulse.
        """
        delta_v = abs(voltage_before_pulse_v - voltage_during_pulse_v)
        delta_i = max(1.0, abs(current_pulse_amperes))

        dcir_ohms = delta_v / delta_i
        dcir_mohm = dcir_ohms * 1000.0

        degradation_factor = dcir_mohm / BatteryInternalResistanceEstimator.BASELINE_DCIR_MOHM
        needs_replacement = dcir_mohm >= BatteryInternalResistanceEstimator.MAX_ALLOWABLE_DCIR_MOHM

        return {
            'measured_dcir_mohm': round(dcir_mohm, 2),
            'baseline_dcir_mohm': BatteryInternalResistanceEstimator.BASELINE_DCIR_MOHM,
            'resistance_growth_factor': round(degradation_factor, 2),
            'pack_power_delivery_capability_pct': max(10.0, min(100.0, round((1.0 / degradation_factor) * 100.0, 1))),
            'battery_module_health': 'REPLACE_DEGRADED_MODULE' if needs_replacement else 'HEALTHY_NOMINAL'
        }
