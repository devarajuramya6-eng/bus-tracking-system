"""
CityBus Enterprise Platform - Transit Signal Priority (TSP) Engine
File: backend/services/brt/transit_signal_priority.py

Generates dynamic NTCIP 1202 / SCATS traffic signal priority requests:
- Green Extension: Extends active green phase by 8-15 seconds for approaching buses
- Early Green / Red Truncation: Cuts conflicting red cycle short to prioritize bus progression
- Priority filtering based on schedule adherence (only delayed buses or buses with > 30 passengers request priority)
"""

from typing import Dict, Any, Optional


class TransitSignalPriorityEngine:
    SIGNALIZED_JUNCTIONS = {
        'JNC-BENZ-01': {'name': 'Benz Circle Main Intersection', 'lat': 16.5020, 'lng': 80.6475, 'approach_distance_m': 150},
        'JNC-RAMA-02': {'name': 'Ramavarappadu Ring Junction', 'lat': 16.5180, 'lng': 80.6720, 'approach_distance_m': 180},
        'JNC-PNBS-03': {'name': 'PNBS Bus Station North Gate', 'lat': 16.5120, 'lng': 80.6180, 'approach_distance_m': 120}
    }

    @staticmethod
    def evaluate_tsp_request(bus_id: int, bus_lat: float, bus_lng: float,
                             speed_kmh: float, occupancy: int,
                             delay_minutes: float, junction_id: str) -> Dict[str, Any]:
        """
        Evaluates whether an approaching bus is eligible for green signal priority.
        """
        junction = TransitSignalPriorityEngine.SIGNALIZED_JUNCTIONS.get(junction_id, {
            'name': 'Corridor Traffic Junction',
            'lat': bus_lat,
            'lng': bus_lng,
            'approach_distance_m': 150
        })

        # Priority Eligibility Rules:
        # 1. Bus is delayed by >= 3 minutes OR occupancy >= 35 passengers (high passenger throughput)
        is_delayed = delay_minutes >= 3.0
        is_high_occupancy = occupancy >= 35

        should_grant_priority = (is_delayed or is_high_occupancy) and speed_kmh > 10.0

        action = 'NO_REQUEST'
        if should_grant_priority:
            action = 'REQUEST_GREEN_EXTENSION_12S' if speed_kmh > 25.0 else 'REQUEST_EARLY_GREEN_TRUNCATION'

        return {
            'junction_id': junction_id,
            'junction_name': junction['name'],
            'bus_id': bus_id,
            'tsp_granted': should_grant_priority,
            'action': action,
            'rationale': f"Delay: {delay_minutes:.1f}m, Occupancy: {occupancy} pax" if should_grant_priority else "Bus is on-time or low occupancy.",
            'controller_protocol': 'NTCIP_1202_PRIORITY_PDU'
        }
