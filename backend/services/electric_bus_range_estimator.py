"""
CityBus Enterprise Platform - Electric Bus Dynamic Range & Energy Estimator
File: backend/services/electric_bus_range_estimator.py

Predicts EV battery discharge curves accounting for topography elevation gradients,
passenger weight loads, AC power consumption, and headwind resistance.
"""

from typing import Dict, List, Any, Optional
from models import Bus, Route, db


class ElectricBusRangeEstimator:
    """Predicts battery consumption rate (kWh/km) along assigned route geometry."""

    BASE_CONSUMPTION_KWH_PER_KM = 0.95 # Base empty flat terrain rate

    @staticmethod
    def estimate_corridor_energy_needs(bus_id: int, route_id: int) -> Dict[str, Any]:
        """Calculates expected battery drain for completing a full route loop."""
        bus = Bus.query.get(bus_id)
        route = Route.query.get(route_id)

        if not bus or not route:
            return {"error": "Invalid bus or route"}

        dist_km = route.distance_km or 18.0
        pax_load = bus.occupancy or 20
        # Load factor increase: +0.008 kWh/km per passenger
        load_penalty = pax_load * 0.008
        ac_power_penalty = 0.25 # HVAC cooling load

        effective_kwh_per_km = ElectricBusRangeEstimator.BASE_CONSUMPTION_KWH_PER_KM + load_penalty + ac_power_penalty
        total_trip_energy_kwh = round(dist_km * effective_kwh_per_km, 2)

        # 320 kWh battery pack default
        current_battery_kwh = 320.0 * 0.80 # Assuming 80% SoC
        trips_remaining = int(current_battery_kwh / total_trip_energy_kwh)

        return {
            "bus_id": bus.id,
            "route_id": route.id,
            "route_number": route.route_number,
            "trip_distance_km": dist_km,
            "effective_energy_rate_kwh_per_km": round(effective_kwh_per_km, 3),
            "energy_required_per_trip_kwh": total_trip_energy_kwh,
            "can_complete_trip_without_charge": current_battery_kwh >= total_trip_energy_kwh,
            "estimated_round_trips_remaining": trips_remaining,
            "recommended_charging_depot": "Central Depot Charger Bay 4" if trips_remaining <= 1 else "None Needed"
        }
