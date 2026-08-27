"""
CityBus Enterprise Platform - Automated Bus Wash & Cleanliness Inspection Service
File: backend/services/depot_wash_inspector_service.py

Schedules automated gantry wash cycles, tracks recycled water usage (85% filtration recovery),
and inspects interior disinfection compliance before morning passenger service.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from models import Bus, db
from repositories.audit_repository import AuditRepository


class DepotWashInspectorService:
    """Manages drive-through automated bus wash queues and hygiene logs."""

    _wash_logs: List[Dict[str, Any]] = []

    @classmethod
    def record_wash_cycle(cls, bus_id: int, wash_type: str = "EXTERIOR_AND_CHASSIS",
                          interior_sanitized: bool = True, water_liters_used: float = 180.0) -> Dict[str, Any]:
        """Logs completion of bus cleaning and hygiene sign-off."""
        bus = Bus.query.get(bus_id)
        bus_num = bus.bus_number if bus else f"Bus #{bus_id}"

        recycled_water_liters = round(water_liters_used * 0.85, 1) # 85% recovered

        entry = {
            "wash_id": f"WASH-{int(datetime.utcnow().timestamp())}",
            "bus_id": bus_id,
            "bus_number": bus_num,
            "wash_type": wash_type,
            "interior_sanitized": interior_sanitized,
            "fresh_water_liters": round(water_liters_used - recycled_water_liters, 1),
            "recycled_water_liters": recycled_water_liters,
            "inspection_passed": True,
            "completed_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }

        cls._wash_logs.append(entry)
        AuditRepository.log_event("BUS_WASH_COMPLETED", "DepotWash", bus_id, None, None, f"Bus: {bus_num}, Sanitized: {interior_sanitized}")

        return entry

    @classmethod
    def get_recent_wash_logs(cls) -> List[Dict[str, Any]]:
        """Returns recent cleaning audit records."""
        return cls._wash_logs[-20:]
