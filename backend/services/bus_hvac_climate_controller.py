"""
CityBus Enterprise Platform - On-Bus HVAC & Climate Automation Service
File: backend/services/bus_hvac_climate_controller.py

Regulates interior bus temperature setpoints (22°C to 24°C standard),
monitors cabin CO2 parts-per-million (fresh air intake damper control), and manages compressor power draw.
"""

from typing import Dict, List, Any, Optional


class BusHVACClimateController:
    """Automates vehicle air conditioning, air purification filters, and thermal efficiency."""

    @staticmethod
    def get_cabin_climate_status(bus_id: int, ambient_temp_c: float = 36.0, occupancy: int = 25) -> Dict[str, Any]:
        """Calculates cooling demand and cabin ventilation fresh air damper angle."""
        target_setpoint = 23.0 # Standard 23°C
        cooling_load_kw = max(2.5, (ambient_temp_c - target_setpoint) * 0.8 + (occupancy * 0.12))

        # Cabin CO2 parts per million estimation
        cabin_co2_ppm = min(1800, 450 + (occupancy * 32))
        damper_opening_pct = 45 if cabin_co2_ppm > 1000 else 20

        return {
            "bus_id": bus_id,
            "ambient_outside_temp_c": ambient_temp_c,
            "cabin_interior_temp_c": round(target_setpoint + 0.5, 1),
            "target_setpoint_temp_c": target_setpoint,
            "cabin_co2_ppm": cabin_co2_ppm,
            "fresh_air_damper_opening_pct": damper_opening_pct,
            "air_purification_filter_status": "HEPA_FILTER_ACTIVE",
            "hvac_compressor_power_kw": round(cooling_load_kw, 1),
            "fan_blower_speed": "MEDIUM"
        }
