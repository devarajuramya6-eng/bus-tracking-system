"""
CityBus Enterprise Platform - EV Lithium-Ion Battery Degradation Model
File: backend/services/ev/battery_degradation_model.py

Models traction battery capacity fade and State of Health (SoH %):
- Cycle Aging (Depth of Discharge DoD exponential model)
- Calendar Aging (Arrhenius temperature degradation for hot climate zones)
- Fast DC charging C-rate stress factors
"""

import math
from typing import Dict, Any


class BatteryDegradationModel:
    @staticmethod
    def estimate_soh(equivalent_full_cycles: int,
                     avg_ambient_temp_c: float = 34.0,
                     fast_charge_ratio: float = 0.35) -> Dict[str, Any]:
        """
        Estimates remaining battery State of Health (SoH %).
        :param equivalent_full_cycles: Cumulative charge/discharge cycles
        :param avg_ambient_temp_c: Average ambient operating temperature
        :param fast_charge_ratio: Fraction of charging done on DC fast chargers (> 100 kW)
        """
        # Base cycle degradation: approx 0.005% per cycle under standard 25C
        cycle_fade = equivalent_full_cycles * 0.0048

        # Temperature acceleration factor (Arrhenius law relative to 25C reference)
        delta_temp = max(0.0, avg_ambient_temp_c - 25.0)
        temp_multiplier = 1.0 + (delta_temp * 0.025)

        # C-rate fast charge penalty (high C-rate induces lithium plating)
        fast_charge_penalty = 1.0 + (fast_charge_ratio * 0.20)

        total_capacity_loss_pct = cycle_fade * temp_multiplier * fast_charge_penalty
        soh_pct = max(60.0, min(100.0, 100.0 - total_capacity_loss_pct))

        # Remaining useful life (RUL) estimation (Retirement threshold 75% SoH)
        remaining_soh_to_limit = max(0.0, soh_pct - 75.0)
        cycles_remaining = int((remaining_soh_to_limit / (0.0048 * temp_multiplier * fast_charge_penalty))) if soh_pct > 75.0 else 0

        return {
            'soh_percentage': round(soh_pct, 2),
            'capacity_loss_percentage': round(100.0 - soh_pct, 2),
            'equivalent_cycles': equivalent_full_cycles,
            'estimated_cycles_remaining': cycles_remaining,
            'battery_status': 'EXCELLENT' if soh_pct >= 90 else ('GOOD' if soh_pct >= 80 else ('DEGRADED' if soh_pct >= 75 else 'REPLACE_REQUIRED'))
        }
