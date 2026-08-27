from typing import Dict, List, Any

class IntercityCorridorFeederService:
    """Coordinates high-capacity intercity express links between Vijayawada, Guntur, and Tenali."""

    CORRIDORS = [
        {"corridor_id": "EXP-VJA-GNT", "name": "Amaravati Expressway Non-Stop", "distance_km": 34.5, "avg_travel_time_min": 42, "daily_frequency_minutes": 10},
        {"corridor_id": "EXP-VJA-AIR", "name": "Gannavaram Airport Metro Shuttle", "distance_km": 21.0, "avg_travel_time_min": 30, "daily_frequency_minutes": 15},
        {"corridor_id": "EXP-VJA-TNL", "name": "Tenali Agricultural Belt Feeder", "distance_km": 38.0, "avg_travel_time_min": 50, "daily_frequency_minutes": 20}
    ]

    @staticmethod
    def get_corridor_overview() -> List[Dict[str, Any]]:
        return IntercityCorridorFeederService.CORRIDORS
