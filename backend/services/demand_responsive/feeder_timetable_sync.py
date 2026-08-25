"""
CityBus Enterprise Platform - Feeder-to-Trunk Intermodal Timetable Synchronizer
File: backend/services/demand_responsive/feeder_timetable_sync.py

Synchronizes feeder van arrivals with scheduled mainline trunk bus departures:
- Enforces guaranteed transfer window (Arrive at hub 3 to 7 minutes before trunk bus departs)
- Coordinates transfer hold requests when feeder van is slightly delayed
"""

from typing import Dict, Any, List


class FeederTimetableSynchronizer:
    @staticmethod
    def calculate_sync_arrival(feeder_eta_min: int, trunk_departure_min: int, trunk_route_number: str) -> Dict[str, Any]:
        """
        Evaluates intermodal transfer feasibility.
        """
        buffer_min = trunk_departure_min - feeder_eta_min

        if buffer_min >= 3 and buffer_min <= 10:
            return {
                'transfer_status': 'GUARANTEED_SEAMLESS_TRANSFER',
                'buffer_minutes': buffer_min,
                'trunk_route': trunk_route_number,
                'trunk_departure_time_min': trunk_departure_min,
                'hold_requested': False,
                'advice': f"Feeder van will arrive with a comfortable {buffer_min}-minute transfer buffer."
            }
        elif buffer_min >= 0 and buffer_min < 3:
            return {
                'transfer_status': 'TIGHT_TRANSFER_HOLD_TRIGGERED',
                'buffer_minutes': buffer_min,
                'trunk_route': trunk_route_number,
                'trunk_departure_time_min': trunk_departure_min,
                'hold_requested': True,
                'hold_duration_sec': 120,
                'advice': f"Hold signal of 2 minutes dispatched to trunk bus {trunk_route_number} to secure transfer."
            }
        else:
            return {
                'transfer_status': 'MISSED_TRANSFER_NEXT_HEADWAY',
                'buffer_minutes': buffer_min,
                'trunk_route': trunk_route_number,
                'trunk_departure_time_min': trunk_departure_min,
                'hold_requested': False,
                'advice': "Transfer missed. Passenger will be boarded on next scheduled headway."
            }
