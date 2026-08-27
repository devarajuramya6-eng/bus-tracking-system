"""
CityBus Enterprise Platform - Depot Yard Operations & Bay Management Service
File: backend/services/depot_operations_service.py

Coordinates overnight fleet parking slots, electric pantograph/plug-in chargers,
automatic drive-through bus wash queues, and morning pull-out dispatch sequencing.
"""

from typing import Dict, List, Any, Optional, Tuple
from models import Bus, MaintenanceWorkOrder, db
from repositories.audit_repository import AuditRepository


class DepotParkingSlot:
    def __init__(self, slot_id: str, bay_type: str, has_ev_charger: bool = False, max_length_meters: float = 12.0):
        self.slot_id = slot_id
        self.bay_type = bay_type  # STANDARD_PARKING, EV_CHARGING_BAY, MAINTENANCE_BAY, WASH_BAY
        self.has_ev_charger = has_ev_charger
        self.assigned_bus_id: Optional[int] = None
        self.is_occupied = False


class DepotOperationsService:
    """Manages physical depot yard topology and automated overnight slot assignments."""

    _yard_slots: Dict[str, DepotParkingSlot] = {
        f"BAY-EV-{i:02d}": DepotParkingSlot(f"BAY-EV-{i:02d}", "EV_CHARGING_BAY", True) for i in range(1, 16)
    }
    _yard_slots.update({
        f"BAY-STD-{i:02d}": DepotParkingSlot(f"BAY-STD-{i:02d}", "STANDARD_PARKING", False) for i in range(1, 36)
    })
    _yard_slots.update({
        f"BAY-MAINT-{i:02d}": DepotParkingSlot(f"BAY-MAINT-{i:02d}", "MAINTENANCE_BAY", False) for i in range(1, 6)
    })
    _yard_slots.update({
        "WASH-01": DepotParkingSlot("WASH-01", "WASH_BAY", False)
    })

    @classmethod
    def get_yard_occupancy_matrix(cls) -> Dict[str, Any]:
        """Returns visual map of all depot parking bays, charger states, and docked buses."""
        total_slots = len(cls._yard_slots)
        occupied_count = sum(1 for s in cls._yard_slots.values() if s.is_occupied)
        ev_chargers_active = sum(1 for s in cls._yard_slots.values() if s.has_ev_charger and s.is_occupied)

        slots_data = []
        for s_id, slot in cls._yard_slots.items():
            bus_num = None
            if slot.assigned_bus_id:
                b = Bus.query.get(slot.assigned_bus_id)
                bus_num = b.bus_number if b else None

            slots_data.append({
                "slot_id": slot.slot_id,
                "bay_type": slot.bay_type,
                "has_ev_charger": slot.has_ev_charger,
                "is_occupied": slot.is_occupied,
                "assigned_bus_id": slot.assigned_bus_id,
                "assigned_bus_number": bus_num
            })

        return {
            "total_depot_bays": total_slots,
            "occupied_bays": occupied_count,
            "available_bays": total_slots - occupied_count,
            "active_ev_charging_sessions": ev_chargers_active,
            "bays": slots_data
        }

    @classmethod
    def assign_vehicle_to_bay(cls, bus_id: int) -> Tuple[Optional[str], Optional[str]]:
        """Automatically assigns the optimal parking/charging bay upon evening depot check-in."""
        bus = Bus.query.get(bus_id)
        if not bus:
            return None, "Bus not found"

        # Check if already assigned
        for s_id, slot in cls._yard_slots.items():
            if slot.assigned_bus_id == bus_id:
                return s_id, None

        # Check if bus requires maintenance
        has_open_maint = MaintenanceWorkOrder.query.filter_by(bus_id=bus_id, status='OPEN').count() > 0
        preferred_type = "MAINTENANCE_BAY" if has_open_maint else ("EV_CHARGING_BAY" if bus.fuel_type == "Electric" else "STANDARD_PARKING")

        # Find empty slot matching preference
        target_slot = None
        for s_id, slot in cls._yard_slots.items():
            if not slot.is_occupied and slot.bay_type == preferred_type:
                target_slot = slot
                break

        # Fallback to standard parking if preferred full
        if not target_slot:
            for s_id, slot in cls._yard_slots.items():
                if not slot.is_occupied and slot.bay_type == "STANDARD_PARKING":
                    target_slot = slot
                    break

        if not target_slot:
            return None, "Depot yard is currently at full capacity"

        target_slot.is_occupied = True
        target_slot.assigned_bus_id = bus_id
        bus.status = "Offline"
        db.session.commit()

        AuditRepository.log_event("DEPOT_BAY_ASSIGNED", "DepotBay", target_slot.slot_id, None, None, f"Bus: {bus.bus_number}")

        return target_slot.slot_id, None

    @classmethod
    def release_bay(cls, slot_id: str) -> bool:
        """Releases parking slot for morning pull-out dispatch."""
        slot = cls._yard_slots.get(slot_id)
        if not slot:
            return False

        slot.is_occupied = False
        slot.assigned_bus_id = None
        return True
