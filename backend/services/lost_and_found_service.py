"""
CityBus Enterprise Platform - Transit Lost & Found Property Service
File: backend/services/lost_and_found_service.py

Manages passenger property left behind on buses, conductor intake logging,
depot safe storage inventory, and passenger retrieval verification.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from repositories.audit_repository import AuditRepository


class LostPropertyItem:
    def __init__(self, item_id: int, bus_id: int, category: str, description: str,
                 found_by_name: str, found_date: Optional[datetime] = None):
        self.item_id = item_id
        self.bus_id = bus_id
        self.category = category # Electronics, Bag/Luggage, Wallet/ID, Apparel, Documents
        self.description = description
        self.found_by_name = found_by_name
        self.found_date = found_date or datetime.utcnow()
        self.status = "IN_DEPOT_SAFE" # IN_DEPOT_SAFE, CLAIMED, TRANSFERRED_TO_POLICE
        self.claimed_by_user_id: Optional[int] = None
        self.claim_notes: Optional[str] = None


class LostAndFoundService:
    """Manages inventory of items found on transit vehicles."""

    _items_db: Dict[int, LostPropertyItem] = {}
    _counter = 1

    @classmethod
    def register_found_item(cls, bus_id: int, category: str, description: str, found_by_name: str) -> Dict[str, Any]:
        """Logs a new item retrieved by conductor or cleaner."""
        item_id = cls._counter
        cls._counter += 1

        item = LostPropertyItem(item_id, bus_id, category, description, found_by_name)
        cls._items_db[item_id] = item

        AuditRepository.log_event("LOST_ITEM_REGISTERED", "LostProperty", item_id, None, None, f"Category: {category}")

        return {
            "item_id": item.item_id,
            "bus_id": item.bus_id,
            "category": item.category,
            "description": item.description,
            "status": item.status,
            "found_date": item.found_date.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def search_items(cls, category: Optional[str] = None, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """Searches unclaimed items in depot safe."""
        results = []
        for item in cls._items_db.values():
            if item.status == "IN_DEPOT_SAFE":
                if category and category.lower() != 'all' and item.category.lower() != category.lower():
                    continue
                if keyword and keyword.lower() not in item.description.lower():
                    continue

                results.append({
                    "item_id": item.item_id,
                    "bus_id": item.bus_id,
                    "category": item.category,
                    "description": item.description,
                    "found_date": item.found_date.strftime("%Y-%m-%d"),
                    "status": item.status
                })
        return results

    @classmethod
    def claim_item(cls, item_id: int, user_id: int, claimant_notes: str) -> Tuple[bool, Optional[str]]:
        """Processes passenger claim for a lost item."""
        item = cls._items_db.get(item_id)
        if not item:
            return False, "Item not found"
        if item.status != "IN_DEPOT_SAFE":
            return False, f"Item is already marked as {item.status}"

        item.status = "CLAIMED"
        item.claimed_by_user_id = user_id
        item.claim_notes = claimant_notes

        AuditRepository.log_event("LOST_ITEM_CLAIMED", "LostProperty", item_id, user_id, None, f"Notes: {claimant_notes}")
        return True, None
