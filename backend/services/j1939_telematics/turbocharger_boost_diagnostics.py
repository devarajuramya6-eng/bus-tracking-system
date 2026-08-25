"""
CityBus Enterprise Platform - Diesel Turbocharger Boost & EGT Diagnostics
File: backend/services/j1939_telematics/turbocharger_boost_diagnostics.py

Monitors intake manifold pressure and exhaust gas temperature:
- Intake Manifold 1 Pressure (SPN 102, Boost bar/PSI)
- Engine Exhaust Gas Temperature (SPN 173, EGT °C)
- Detects boost leaks and intercooler hose ruptures (Low boost under high throttle demand)
"""

from typing import Dict, Any


class TurbochargerBoostDiagnostics:
    NOMINAL_MAX_BOOST_BAR = 2.4
    MAX_SAFE_EGT_C = 680.0

    @staticmethod
    def audit_boost_performance(engine_load_pct: float, boost_pressure_bar: float, egt_c: float) -> Dict[str, Any]:
        """
        Diagnoses turbocharger pressure and thermal efficiency.
        """
        # If engine is under > 80% full load, boost should be > 1.6 bar
        is_underboosting = engine_load_pct >= 80.0 and boost_pressure_bar < 1.4
        is_egt_critical = egt_c >= TurbochargerBoostDiagnostics.MAX_SAFE_EGT_C

        status = 'CRITICAL_EGT_THERMAL_ALERT' if is_egt_critical else ('BOOST_LEAK_DETECTED' if is_underboosting else 'BOOST_SYSTEM_NOMINAL')

        return {
            'engine_load_pct': round(engine_load_pct, 1),
            'boost_pressure_bar': round(boost_pressure_bar, 2),
            'boost_pressure_psi': round(boost_pressure_bar * 14.5038, 1),
            'exhaust_gas_temp_celsius': round(egt_c, 1),
            'is_boost_leak_suspected': is_underboosting,
            'is_excessive_egt': is_egt_critical,
            'diagnostics_state': status
        }
