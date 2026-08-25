"""
CityBus Enterprise Platform - Dual-Beam Infrared Doorway APC Sensor
File: backend/services/apc/infrared_door_sensor.py

Processes dual-beam optical doorway sensors for passenger counting:
- Beam A (Outer) and Beam B (Inner) time-sequence discrimination
- Sequence: Beam A ➔ Beam B triggers Passenger IN (Boarding)
- Sequence: Beam B ➔ Beam A triggers Passenger OUT (Alighting)
- Multi-door aggregation (Front boarding door + Rear alighting door)
"""

import time
from typing import Dict, Any, List


class InfraredDoorSensor:
    """Decodes dual-beam doorway break sequence."""

    @staticmethod
    def process_beam_events(door_id: str, beam_a_timestamp: float, beam_b_timestamp: float) -> Dict[str, Any]:
        """
        Determines direction of passenger passage.
        """
        delta_t = beam_b_timestamp - beam_a_timestamp

        # If Beam A broken first (delta_t > 0), passenger moved from Outside ➔ Inside (Boarding)
        if 0.02 <= delta_t <= 1.2: # Nominal passage duration 20ms to 1200ms
            return {
                'door_id': door_id,
                'event_type': 'PASSENGER_BOARDING_IN',
                'delta_seconds': round(delta_t, 3),
                'count_change': +1,
                'confidence': 0.98
            }
        # If Beam B broken first (delta_t < 0), passenger moved from Inside ➔ Outside (Alighting)
        elif -1.2 <= delta_t <= -0.02:
            return {
                'door_id': door_id,
                'event_type': 'PASSENGER_ALIGHTING_OUT',
                'delta_seconds': round(abs(delta_t), 3),
                'count_change': -1,
                'confidence': 0.98
            }

        return {
            'door_id': door_id,
            'event_type': 'OPTICAL_NOISE_IGNORED',
            'count_change': 0,
            'confidence': 0.10
        }
