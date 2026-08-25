"""
CityBus Enterprise Platform - Electric Bus Fleet & Charging Management Service
File: backend/services/ev_charging_service.py

Monitors EV fleet battery telemetry:
- State of Charge (SoC %)
- Estimated remaining operational range (km)
- Smart depot charger scheduling (Fast DC 120kW chargers at PNBS & Autonagar depots)
"""

from models import db, Bus


class EVChargingService:
    @staticmethod
    def get_ev_fleet_status():
        """Returns battery telemetry and charging statuses for all electric buses."""
        buses = Bus.query.all()
        ev_data = []

        for b in buses:
            # Deterministic simulation based on bus ID
            soc_pct = max(18, 98 - (b.id * 3) % 80)
            range_km = int(soc_pct * 2.8) # Approx 2.8 km per 1% SoC on 320 kWh battery pack
            charging_status = 'In Transit'
            if soc_pct < 25:
                charging_status = 'Charging (Depot Bay #3)'

            ev_data.append({
                'bus_id': b.id,
                'bus_number': b.bus_number,
                'model': b.model,
                'battery_capacity_kwh': 320,
                'soc_percentage': soc_pct,
                'estimated_range_km': range_km,
                'status': charging_status,
                'battery_health_soh': 96.5,
                'temperature_celsius': 32.4
            })

        return ev_data
