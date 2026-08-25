"""
CityBus Enterprise Platform - EV Regenerative Braking & Energy Recovery Analyzer
File: backend/services/ev/regenerative_braking_analyzer.py

Analyzes kinetic energy recovery during urban bus braking:
- Evaluates stop frequency and deceleration profiles
- Calculates net kWh/km consumption with regen capture
"""

from typing import List, Dict, Any


class RegenerativeBrakingAnalyzer:
    @staticmethod
    def analyze_trip_energy(distance_km: float, stops_count: int, avg_speed_kmh: float = 24.0, bus_weight_tonnes: float = 14.5) -> Dict[str, Any]:
        """
        Computes gross energy demand and regenerative braking energy recovery.
        """
        # Baseline gross traction energy: approx 1.18 kWh per km for 14.5t bus
        gross_traction_kwh = distance_km * 1.18

        # Kinetic energy recovery per stop brake event (approx 0.12 kWh recovered per deceleration to zero)
        regen_efficiency = 0.65 # 65% motor/inverter round-trip capture
        regen_recovered_kwh = stops_count * 0.12 * regen_efficiency

        # HVAC and auxiliary load (AC compressor, air brakes, power steering, telematics: approx 8 kW continuous)
        trip_hours = distance_km / max(10.0, avg_speed_kmh)
        auxiliary_kwh = trip_hours * 8.0

        net_energy_kwh = gross_traction_kwh - regen_recovered_kwh + auxiliary_kwh
        net_kwh_per_km = net_energy_kwh / max(0.1, distance_km)

        return {
            'distance_km': round(distance_km, 2),
            'stops_count': stops_count,
            'gross_traction_kwh': round(gross_traction_kwh, 2),
            'regen_recovered_kwh': round(regen_recovered_kwh, 2),
            'auxiliary_load_kwh': round(auxiliary_kwh, 2),
            'net_energy_consumed_kwh': round(net_energy_kwh, 2),
            'efficiency_kwh_per_km': round(net_kwh_per_km, 2),
            'regen_savings_percentage': round((regen_recovered_kwh / gross_traction_kwh) * 100.0, 1) if gross_traction_kwh > 0 else 0.0
        }
