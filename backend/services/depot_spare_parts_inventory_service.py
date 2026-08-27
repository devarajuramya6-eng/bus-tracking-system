"""
CityBus Enterprise Platform - Depot Spare Parts Inventory & Stock Service
File: backend/services/depot_spare_parts_inventory_service.py

Tracks warehouse stock of brake pads, suspension air springs, coolant drums,
EV charging cables, filters, and issues low-stock purchase requisitions.
"""

from typing import Dict, List, Any, Optional, Tuple
from repositories.audit_repository import AuditRepository


class SparePartItem:
    def __init__(self, part_id: str, name: str, category: str, unit_price_inr: float,
                 stock_quantity: int, min_reorder_level: int = 10):
        self.part_id = part_id
        self.name = name
        self.category = category  # Brakes, Powertrain, Electrical/EV, Suspension, Fluids
        self.unit_price_inr = unit_price_inr
        self.stock_quantity = stock_quantity
        self.min_reorder_level = min_reorder_level


class DepotSparePartsInventoryService:
    """Manages physical spare parts inventory across central bus maintenance workshops."""

    _inventory: Dict[str, SparePartItem] = {
        "PRT-BRK-01": SparePartItem("PRT-BRK-01", "Heavy Duty Ceramic Brake Pad Set", "Brakes", 3200.0, 42, 15),
        "PRT-SUS-02": SparePartItem("PRT-SUS-02", "Air Bellow Suspension Spring", "Suspension", 7500.0, 18, 8),
        "PRT-EV-03":  SparePartItem("PRT-EV-03", "CCS2 DC Fast Charging Connector Cable", "Electrical/EV", 18500.0, 6, 4),
        "PRT-ENG-04": SparePartItem("PRT-ENG-04", "BS-VI Diesel Particulate Filter (DPF)", "Powertrain", 24000.0, 9, 5),
        "PRT-OIL-05": SparePartItem("PRT-OIL-05", "15W-40 Synthetic Engine Oil (20L Drum)", "Fluids", 4800.0, 28, 10),
        "PRT-TYR-06": SparePartItem("PRT-TYR-06", "295/80 R22.5 Commercial Radial Tire", "Wheels", 16500.0, 34, 12)
    }

    @classmethod
    def get_all_parts(cls) -> List[Dict[str, Any]]:
        """Returns catalog of all stocked parts and reorder flags."""
        result = []
        for p in cls._inventory.values():
            result.append({
                "part_id": p.part_id,
                "name": p.name,
                "category": p.category,
                "unit_price_inr": p.unit_price_inr,
                "stock_quantity": p.stock_quantity,
                "min_reorder_level": p.min_reorder_level,
                "is_low_stock": p.stock_quantity <= p.min_reorder_level
            })
        return result

    @classmethod
    def consume_part_for_work_order(cls, part_id: str, quantity: int, work_order_id: int) -> Tuple[bool, Optional[str]]:
        """Deducts spare parts from inventory upon technician installation."""
        part = cls._inventory.get(part_id)
        if not part:
            return False, "Part not found"
        if part.stock_quantity < quantity:
            return False, f"Insufficient stock ({part.stock_quantity} available, {quantity} requested)"

        part.stock_quantity -= quantity
        AuditRepository.log_event("SPARE_PART_CONSUMED", "SparePart", part_id, None, None, f"Qty: {quantity}, WorkOrder: {work_order_id}")
        return True, None

    @classmethod
    def restock_part(cls, part_id: str, quantity: int, invoice_ref: str) -> Tuple[bool, Optional[str]]:
        """Adds newly delivered warehouse stock."""
        part = cls._inventory.get(part_id)
        if not part:
            return False, "Part not found"

        part.stock_quantity += quantity
        AuditRepository.log_event("SPARE_PART_RESTOCKED", "SparePart", part_id, None, None, f"Qty: {quantity}, Inv: {invoice_ref}")
        return True, None
