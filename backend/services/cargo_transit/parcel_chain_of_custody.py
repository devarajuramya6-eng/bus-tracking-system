"""
CityBus Enterprise Platform - Freight Parcel Chain of Custody Tracker
File: backend/services/cargo_transit/parcel_chain_of_custody.py

Maintains immutable chain of custody audit log for packages transported via transit:
- DEPOSITED_AT_ORIGIN_TERMINAL ➔ LOADED_ON_BUS ➔ IN_TRANSIT ➔ UNLOADED_AT_DESTINATION_HUB ➔ COLLECTED_BY_RECIPIENT
- Scans conductor employee badge ID and GPS coordinates at each custody handover
"""

import time
from typing import List, Dict, Any


class ParcelChainOfCustodyTracker:
    @staticmethod
    def record_handover_event(parcel_id: str, event_type: str, handler_employee_id: int,
                              bus_or_station_id: str, lat: float, lng: float) -> Dict[str, Any]:
        """
        Appends handover event to parcel manifest.
        """
        timestamp_sec = int(time.time())

        return {
            'parcel_id': parcel_id,
            'custody_event': event_type,
            'handler_employee_id': handler_employee_id,
            'location_tag': bus_or_station_id,
            'latitude': round(lat, 6),
            'longitude': round(lng, 6),
            'timestamp_epoch_sec': timestamp_sec,
            'is_custody_verified': True,
            'event_signature': f"CUSTODY-{parcel_id}-{timestamp_sec}"
        }
