"""
CityBus Enterprise Platform - Multi-Zone Tri-City Transit Fare Matrix
File: backend/services/multi_zone_fare_matrix.py

Manages geographic fare zones across the Capital Metropolitan Region:
- Zone 1: Vijayawada Core Urban Belt
- Zone 2: Guntur Urban Municipal Area
- Zone 3: Amaravati Capital Government Complex
- Zone 4: Gannavaram Airport & Tech Industrial Corridor
"""

from typing import Dict, List, Any, Optional


class MultiZoneFareMatrix:
    """Calculates cross-zone boundary pricing multipliers and zone pass rules."""

    ZONES = {
        "ZONE_1_VJA": {"name": "Vijayawada Core City", "base_multiplier": 1.0},
        "ZONE_2_GNT": {"name": "Guntur Municipal Region", "base_multiplier": 1.0},
        "ZONE_3_AMR": {"name": "Amaravati Capital City", "base_multiplier": 1.15},
        "ZONE_4_AIR": {"name": "Gannavaram Airport Express Corridor", "base_multiplier": 1.25}
    }

    # Inter-zone base fare cross-table (INR)
    ZONE_CROSS_TABLE = {
        ("ZONE_1_VJA", "ZONE_1_VJA"): 15.0,
        ("ZONE_1_VJA", "ZONE_2_GNT"): 35.0, # Intercity corridor
        ("ZONE_1_VJA", "ZONE_3_AMR"): 30.0,
        ("ZONE_1_VJA", "ZONE_4_AIR"): 40.0,
        ("ZONE_2_GNT", "ZONE_3_AMR"): 25.0,
        ("ZONE_2_GNT", "ZONE_4_AIR"): 55.0,
        ("ZONE_3_AMR", "ZONE_4_AIR"): 45.0
    }

    @classmethod
    def calculate_interzone_fare(cls, origin_zone: str, dest_zone: str, is_express: bool = False) -> Dict[str, Any]:
        """Calculates multi-zone transit fare."""
        z1 = origin_zone.upper()
        z2 = dest_zone.upper()

        key = (z1, z2) if (z1, z2) in cls.ZONE_CROSS_TABLE else (z2, z1)
        base = cls.ZONE_CROSS_TABLE.get(key, 25.0)

        if is_express:
            base += 10.0 # Express service surcharge

        return {
            "origin_zone": z1,
            "destination_zone": z2,
            "is_express_service": is_express,
            "fare_inr": base,
            "cross_zone_boundary_count": 0 if z1 == z2 else 1
        }
