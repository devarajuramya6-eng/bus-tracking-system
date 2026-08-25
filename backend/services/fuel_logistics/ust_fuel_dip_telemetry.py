"""
CityBus Enterprise Platform - Automatic Tank Gauge (ATG) Underground Fuel Dip Telemetry
File: backend/services/fuel_logistics/ust_fuel_dip_telemetry.py

Monitors magnetostrictive probes in depot underground diesel tanks (UST):
- Fuel level (mm) & Strapping Chart volume conversion (Liters)
- Water bottom detection (mm) - Alarms if water level exceeds 25 mm
- Temperature-compensated volume (15°C standard density reconciliation)
"""

from typing import Dict, Any


class USTFuelDipTelemetryParser:
    MAX_ALLOWABLE_WATER_BOTTOM_MM = 25.0
    TANK_TOTAL_CAPACITY_LITERS = 45000.0

    @staticmethod
    def parse_probe_frame(tank_id: str, fuel_level_mm: float, water_level_mm: float, fuel_temp_c: float) -> Dict[str, Any]:
        """
        Parses ATG telemetry and validates fuel quality.
        """
        # Simplified cylindrical tank volume approximation (0 to 3000 mm)
        fill_ratio = min(1.0, max(0.0, fuel_level_mm / 2800.0))
        gross_volume_liters = fill_ratio * USTFuelDipTelemetryParser.TANK_TOTAL_CAPACITY_LITERS

        # Temp compensation: -0.084% volume per degree C above 15°C
        temp_factor = 1.0 - (0.00084 * (fuel_temp_c - 15.0))
        net_volume_15c_liters = gross_volume_liters * temp_factor

        is_water_contamination = water_level_mm >= USTFuelDipTelemetryParser.MAX_ALLOWABLE_WATER_BOTTOM_MM
        is_low_stock = gross_volume_liters <= (USTFuelDipTelemetryParser.TANK_TOTAL_CAPACITY_LITERS * 0.20)

        status = 'CRITICAL_WATER_CONTAMINATION' if is_water_contamination else ('LOW_STOCK_WARNING' if is_low_stock else 'NOMINAL')

        return {
            'tank_id': tank_id,
            'fuel_level_mm': round(fuel_level_mm, 1),
            'gross_volume_liters': round(gross_volume_liters, 1),
            'net_volume_15c_liters': round(net_volume_15c_liters, 1),
            'water_bottom_mm': round(water_level_mm, 1),
            'fuel_temperature_c': round(fuel_temp_c, 1),
            'fill_percentage': round(fill_ratio * 100.0, 1),
            'is_water_alarm': is_water_contamination,
            'is_reorder_level': is_low_stock,
            'tank_health_state': status
        }
