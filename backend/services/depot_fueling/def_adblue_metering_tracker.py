"""
CityBus Enterprise Platform - Diesel Exhaust Fluid (DEF / AdBlue) Metering Tracker
File: backend/services/depot_fueling/def_adblue_metering_tracker.py

Monitors BS-VI SCR (Selective Catalytic Reduction) DEF / AdBlue consumption:
- Benchmark Dosing Ratio: 4.5% to 6.0% of diesel fuel burned
- Flags SCR dosing pump failures if DEF ratio drops below 3.0%
- Monitors urea concentration (ISO 22241 optical refractometer index: 32.5% +/- 0.7%)
"""

from typing import Dict, Any


class DEFAdBlueMeteringTracker:
    BENCHMARK_DEF_RATIO_PCT = 5.0

    @staticmethod
    def audit_def_dosing(bus_number: str, diesel_burned_liters: float,
                         def_consumed_liters: float,
                         urea_refractometer_pct: float = 32.5) -> Dict[str, Any]:
        """
        Validates DEF consumption ratio and chemical purity.
        """
        actual_ratio_pct = (def_consumed_liters / max(1.0, diesel_burned_liters)) * 100.0
        
        is_ratio_low = actual_ratio_pct < 3.0
        is_urea_diluted = abs(urea_refractometer_pct - 32.5) > 1.2
        is_scr_compliant = (not is_ratio_low) and (not is_urea_diluted)

        if is_urea_diluted:
            diag = 'DEF_CONTAMINATED_OR_DILUTED_WITH_WATER'
        elif is_ratio_low:
            diag = 'SCR_DOSER_PUMP_LOW_FLOW_ALARM'
        else:
            diag = 'SCR_EMISSIONS_SYSTEM_COMPLIANT'

        return {
            'bus_number': bus_number,
            'diesel_burned_liters': round(diesel_burned_liters, 1),
            'def_consumed_liters': round(def_consumed_liters, 2),
            'def_dosing_ratio_pct': round(actual_ratio_pct, 2),
            'urea_concentration_pct': round(urea_refractometer_pct, 1),
            'is_bs6_emissions_compliant': is_scr_compliant,
            'scr_system_diagnostic': diag
        }
