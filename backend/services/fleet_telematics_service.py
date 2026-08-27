"""
CityBus Enterprise Platform - Fleet Telematics & CAN-Bus Service
File: backend/services/fleet_telematics_service.py

Decodes OBD-II / J1939 telematics streams, computes harsh braking/acceleration events,
monitors engine coolant temperatures, and predicts mechanical wear.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from models import Bus, Telemetry, db


class FleetTelematicsService:
    """Processes granular vehicle IoT telemetry and health signals."""

    @staticmethod
    def evaluate_driving_behavior(bus_id: int, speed: float, last_speed: float, delta_time_sec: float) -> Dict[str, Any]:
        """Calculates acceleration/deceleration rates to flag harsh events."""
        if delta_time_sec <= 0:
            return {"status": "normal", "accel_mps2": 0.0}

        # Convert km/h to m/s
        v1 = (last_speed * 1000.0) / 3600.0
        v2 = (speed * 1000.0) / 3600.0
        accel_mps2 = (v2 - v1) / delta_time_sec

        event = "Normal"
        if accel_mps2 > 2.8:
            event = "Harsh Acceleration"
        elif accel_mps2 < -3.5:
            event = "Harsh Braking"

        return {
            "bus_id": bus_id,
            "acceleration_mps2": round(accel_mps2, 2),
            "event": event,
            "is_harsh": event != "Normal"
        }

    @staticmethod
    def get_vehicle_diagnostics(bus_id: int) -> Dict[str, Any]:
        """Simulates OBD-II diagnostic parameters for fleet maintenance dashboard."""
        bus = Bus.query.get(bus_id)
        if not bus:
            return {}

        is_electric = bus.fuel_type == "Electric"
        
        return {
            "bus_id": bus.id,
            "bus_number": bus.bus_number,
            "fuel_type": bus.fuel_type,
            "odometer_km": bus.odometer_km,
            "battery_soc_pct": 84.5 if is_electric else None,
            "fuel_level_pct": 68.0 if not is_electric else None,
            "engine_coolant_temp_c": 88.0,
            "tire_pressure_psi": {"front_left": 110, "front_right": 110, "rear_left": 115, "rear_right": 115},
            "brake_pad_wear_pct": min(85, int((bus.odometer_km % 15000) / 150)),
            "dtc_fault_codes": [] if bus.status != 'Maintenance' else ["P0128: Coolant Temp Below Thermostat", "P0300: Random Misfire"]
        }
