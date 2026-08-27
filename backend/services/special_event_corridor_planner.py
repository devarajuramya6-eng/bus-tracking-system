"""
CityBus Enterprise Platform - Special Event & Surge Corridor Transit Planner
File: backend/services/special_event_corridor_planner.py

Designs temporary shuttle corridors for Amaravati Marathon, Krishna Pushkaralu Pilgrimage,
and international cricket matches with dedicated stadium park-and-ride bus loops.
"""

from typing import Dict, List, Any, Optional


class SpecialEventCorridorPlanner:
    """Plans temporary event bus shuttles and stadium crowd dispersal corridors."""

    SPECIAL_EVENTS_CATALOG = [
        {
            "event_id": "EVT-CRICKET-01",
            "name": "India vs England T20 Match - ACA Stadium",
            "venue": "ACA-VDCA Stadium Mangalagiri",
            "expected_attendance": 35000,
            "dedicated_shuttles_count": 24,
            "pickup_points": ["Pandit Nehru Bus Station", "Benz Circle", "Guntur Bus Stand"],
            "shuttle_frequency_minutes": 5,
            "flat_fare_inr": 30.0
        },
        {
            "event_id": "EVT-PUSHKAR-02",
            "name": "Krishna River Pilgrimage Festival",
            "venue": "Prakasam Barrage Ghats",
            "expected_attendance": 120000,
            "dedicated_shuttles_count": 50,
            "pickup_points": ["Vijayawada Junction", "Auto Nagar Terminal", "Gannavaram"],
            "shuttle_frequency_minutes": 3,
            "flat_fare_inr": 20.0
        }
    ]

    @staticmethod
    def get_special_event_shuttles() -> List[Dict[str, Any]]:
        """Returns active and upcoming special event transit corridors."""
        return SpecialEventCorridorPlanner.SPECIAL_EVENTS_CATALOG
