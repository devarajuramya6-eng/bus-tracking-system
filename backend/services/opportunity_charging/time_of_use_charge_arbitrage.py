"""
CityBus Enterprise Platform - Time-of-Use (ToU) Grid Electricity Charge Arbitrage
File: backend/services/opportunity_charging/time_of_use_charge_arbitrage.py

Schedules depot EV charging during lowest spot electricity tariff windows:
- Off-Peak (23:00 - 05:30): ₹3.60 / kWh (High power 120kW bulk charging)
- Normal (09:00 - 17:00): ₹6.20 / kWh (Terminal opportunity top-ups)
- Peak (18:00 - 22:30): ₹9.80 / kWh (Strictly throttled to peak shaving / zero charging)
"""

from typing import Dict, Any, List


class TimeOfUseChargeOptimizer:
    TOU_TARIFF_INR_PER_KWH = {
        'OFF_PEAK': 3.60,
        'NORMAL': 6.20,
        'PEAK': 9.80
    }

    @staticmethod
    def get_tariff_for_hour(hour: int) -> Dict[str, Any]:
        """
        Returns tariff rate and charging permission for current hour.
        """
        if 23 <= hour or hour < 6:
            tier = 'OFF_PEAK'
            charge_allowed = True
            max_kw = 120.0
        elif 18 <= hour < 23:
            tier = 'PEAK'
            charge_allowed = False # Peak shaving
            max_kw = 0.0
        else:
            tier = 'NORMAL'
            charge_allowed = True
            max_kw = 60.0

        return {
            'hour': hour,
            'tariff_tier': tier,
            'rate_inr_per_kwh': TimeOfUseChargeOptimizer.TOU_TARIFF_INR_PER_KWH[tier],
            'charging_authorized': charge_allowed,
            'max_charger_power_kw': max_kw,
            'strategy': 'BULK_OVERNIGHT_CHARGING' if tier == 'OFF_PEAK' else ('PEAK_SHAVING_AVOID_GRID' if tier == 'PEAK' else 'OPPORTUNITY_TOPUP')
        }
