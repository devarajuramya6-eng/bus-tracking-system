"""
CityBus Enterprise Platform - Dynamic Terminal Platform Bay Assigner
File: backend/services/hub_signage/platform_bay_assignment_engine.py

Allocates terminal platform bays (Bays 1-12 at PNBS) to incoming bus trips:
- Groups regional trunk lines (Guntur, Vijayawada loop, Gannavaram Airport) into dedicated bays
- Dynamically resolves bay congestion conflicts by allocating overflow standby bays
"""

from typing import List, Dict, Any


class PlatformBayAssigner:
    STATIC_BAY_MAPPING = {
        '27A': 'BAY_04',
        '5K': 'BAY_02',
        '100E': 'BAY_01',
        '10': 'BAY_06'
    }

    @staticmethod
    def assign_platform_bay(route_number: str, bus_number: str,
                            occupied_bays: List[str]) -> Dict[str, Any]:
        """
        Assigns conflict-free platform bay.
        """
        primary_bay = PlatformBayAssigner.STATIC_BAY_MAPPING.get(route_number, 'BAY_08')

        if primary_bay in occupied_bays:
            # Find next free bay among 1-12
            assigned_bay = 'BAY_12_OVERFLOW'
            for i in range(1, 13):
                candidate = f"BAY_{i:02d}"
                if candidate not in occupied_bays:
                    assigned_bay = candidate
                    break
            is_conflict_diverted = True
        else:
            assigned_bay = primary_bay
            is_conflict_diverted = False

        return {
            'route_number': route_number,
            'bus_number': bus_number,
            'assigned_platform_bay': assigned_bay,
            'is_diverted_to_overflow': is_conflict_diverted,
            'passenger_bay_sign_text': f"Board {route_number} at {assigned_bay}"
        }
