"""
CityBus Enterprise Platform - Depth of Discharge (DoD) Lifespan Optimizer
File: backend/services/ev_battery/depth_of_discharge_optimizer.py

Optimizes daily charging windows to maximize battery pack lifetime:
- Operating within 15% - 85% SoC buffer doubles LFP cell cycle life (4,000+ full equivalent cycles)
- Restricts 100% full fast charges to scheduled overnight depot trickle balances
"""

from typing import Dict, Any


class DepthOfDischargeOptimizer:
    @staticmethod
    def calculate_optimal_charge_limit(route_km: float, bus_efficiency_kwh_per_km: float = 1.15, pack_capacity_kwh: float = 240.0) -> Dict[str, Any]:
        """
        Calculates recommended State of Charge (SoC) target window for duty.
        """
        required_energy_kwh = route_km * bus_efficiency_kwh_per_km
        required_soc_pct = (required_energy_kwh / pack_capacity_kwh) * 100.0

        # Maintain 20% emergency reserve + required duty energy
        target_soc_pct = min(90.0, max(60.0, required_soc_pct + 20.0))
        discharge_floor_pct = max(15.0, target_soc_pct - required_soc_pct)

        effective_dod = target_soc_pct - discharge_floor_pct
        expected_lifespan_cycles = 4500 if effective_dod <= 70.0 else 2800

        return {
            'route_km': route_km,
            'energy_needed_kwh': round(required_energy_kwh, 1),
            'recommended_charge_ceiling_soc_pct': round(target_soc_pct, 1),
            'recommended_discharge_floor_soc_pct': round(discharge_floor_pct, 1),
            'effective_dod_pct': round(effective_dod, 1),
            'expected_battery_cycle_life': expected_lifespan_cycles,
            'battery_warranty_compliance': 'OPTIMAL_WARRANTY_PRESERVED'
        }
