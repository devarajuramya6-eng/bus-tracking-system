"""
CityBus Enterprise Platform - Fuel & Energy Logistics Service
File: backend/services/fuel_service.py

Tracks diesel refueling logs, EV kilowatt-hour battery charging,
fuel card expense reconciliation, and carbon footprint telemetry.
"""

from typing import Dict, List, Any, Optional, Tuple
from repositories.fuel_repository import FuelRepository
from repositories.bus_repository import BusRepository
from repositories.audit_repository import AuditRepository
from models import FuelLog, Bus, db


class FuelService:
    """Business logic for depot energy management and refueling sessions."""

    @staticmethod
    def get_fuel_analytics() -> Dict[str, Any]:
        """Calculates energy consumption breakdown by diesel vs electric."""
        summary = FuelRepository.get_fleet_fuel_summary()
        recent_logs, _ = FuelRepository.get_all(page=1, per_page=15)
        
        return {
            "fleet_summary": summary,
            "recent_fuel_logs": [l.to_dict() for l in recent_logs]
        }

    @staticmethod
    def log_fuel_transaction(bus_id: int, quantity: float, cost: float, odometer_km: Optional[float] = None,
                             station_location: str = "Central Depot Pump 1", fuel_type: str = "Diesel") -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Records a new fueling event."""
        log, err = FuelRepository.create(
            bus_id=bus_id,
            quantity=quantity,
            cost=cost,
            odometer_km=odometer_km,
            station_location=station_location,
            fuel_type=fuel_type
        )
        if err:
            return None, err

        AuditRepository.log_event("FUEL_LOGGED", "FuelLog", log.id, None, None, f"Bus: {bus_id}, Liters: {quantity}")
        return log.to_dict(), None
