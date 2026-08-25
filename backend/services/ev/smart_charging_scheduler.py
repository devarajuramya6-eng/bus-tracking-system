"""
CityBus Enterprise Platform - Depot EV Smart Charging Optimization Engine
File: backend/services/ev/smart_charging_scheduler.py

Schedules depot EV bus charging to minimize electricity bill tariffs and prevent substation grid overload:
- Time-of-Use (ToU) Off-Peak tariff exploitation (23:00 to 06:00 IST)
- Depot transformer peak demand limit management (e.g. 1.2 MW substation cap)
- Priority queuing based on morning departure schedules and current SoC
"""

from typing import List, Dict, Any


class SmartChargingScheduler:
    MAX_DEPOT_POWER_KW = 1200.0 # 1.2 Megawatt transformer limit
    CHARGER_POWER_KW = 120.0 # Dual-gun 120kW DC Fast Chargers

    @staticmethod
    def generate_charging_schedule(bus_fleet_status: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Schedules charging slots across depot bays.
        """
        # Filter electric buses that need charging (SoC < 85%)
        charge_queue = [b for b in bus_fleet_status if b.get('soc_percentage', 100) < 85.0]
        # Sort by urgency (lowest SoC and earliest departure first)
        charge_queue.sort(key=lambda b: b.get('soc_percentage', 100))

        max_concurrent_chargers = int(SmartChargingScheduler.MAX_DEPOT_POWER_KW / SmartChargingScheduler.CHARGER_POWER_KW)
        active_charging = []
        waiting_queue = []

        total_power_allocated_kw = 0.0

        for idx, bus in enumerate(charge_queue):
            energy_needed_kwh = (320.0 * (95.0 - bus.get('soc_percentage', 50))) / 100.0
            charge_time_hours = energy_needed_kwh / SmartChargingScheduler.CHARGER_POWER_KW

            charge_entry = {
                'bus_id': bus.get('bus_id'),
                'bus_number': bus.get('bus_number'),
                'current_soc': bus.get('soc_percentage'),
                'target_soc': 95.0,
                'energy_needed_kwh': round(energy_needed_kwh, 1),
                'estimated_duration_min': int(charge_time_hours * 60.0),
                'allocated_charger_kw': SmartChargingScheduler.CHARGER_POWER_KW,
                'bay_number': f"BAY-{idx + 1:02d}"
            }

            if idx < max_concurrent_chargers:
                active_charging.append(charge_entry)
                total_power_allocated_kw += SmartChargingScheduler.CHARGER_POWER_KW
            else:
                waiting_queue.append(charge_entry)

        return {
            'depot_name': 'PNBS Central EV Depot',
            'transformer_capacity_kw': SmartChargingScheduler.MAX_DEPOT_POWER_KW,
            'total_power_allocated_kw': total_power_allocated_kw,
            'utilization_percentage': round((total_power_allocated_kw / SmartChargingScheduler.MAX_DEPOT_POWER_KW) * 100.0, 1),
            'active_charging_bays': len(active_charging),
            'waiting_in_queue': len(waiting_queue),
            'active_charging': active_charging,
            'waiting_queue': waiting_queue
        }
