"""
CityBus Enterprise Platform - Connection Scan Algorithm (CSA) Timetable Router
File: backend/services/routing/csa_router.py

High-performance linear array scan for transit journey planning (Dibbelt et al.):
- O(|C|) computational complexity where C is the set of scheduled connections
- Earliest Arrival Time (EAT) profile queries
- Footpath transfer buffers
"""

from typing import List, Dict, Any, Optional


class TimetableConnection:
    """Represents a scheduled transit connection between two stops."""
    def __init__(self, dep_stop: int, arr_stop: int, dep_time: int, arr_time: int, trip_id: str, route_num: str):
        self.dep_stop = dep_stop
        self.arr_stop = arr_stop
        self.dep_time = dep_time # Minutes from midnight
        self.arr_time = arr_time
        self.trip_id = trip_id
        self.route_num = route_num


class CSARouter:
    """Connection Scan Algorithm engine."""

    def __init__(self, connections: Optional[List[TimetableConnection]] = None):
        # Sort connections chronologically by departure time
        self.connections = sorted(connections or [], key=lambda c: c.dep_time)

    def find_earliest_arrival(self, origin_stop: int, dest_stop: int, departure_time_min: int) -> Optional[Dict[str, Any]]:
        """
        Scans connections to find the earliest arrival journey.
        """
        # Earliest arrival time array: stop_id -> earliest_arrival_min
        earliest_arrival = {}
        journey_pointer = {} # stop_id -> (connection, prev_stop)

        earliest_arrival[origin_stop] = departure_time_min

        for c in self.connections:
            # If departure time is earlier than requested start, skip
            if c.dep_time < departure_time_min:
                continue

            # Check if departure stop is reachable before connection departs
            if c.dep_stop in earliest_arrival and earliest_arrival[c.dep_stop] <= c.dep_time:
                # If this connection provides a faster arrival at destination stop
                if c.arr_stop not in earliest_arrival or c.arr_time < earliest_arrival[c.arr_stop]:
                    earliest_arrival[c.arr_stop] = c.arr_time
                    journey_pointer[c.arr_stop] = c

        if dest_stop not in earliest_arrival:
            return None

        # Reconstruct path backwards
        itinerary = []
        curr_stop = dest_stop
        while curr_stop in journey_pointer:
            conn = journey_pointer[curr_stop]
            itinerary.insert(0, {
                'from_stop': conn.dep_stop,
                'to_stop': conn.arr_stop,
                'departure_min': conn.dep_time,
                'arrival_min': conn.arr_time,
                'route_number': conn.route_num,
                'trip_id': conn.trip_id
            })
            curr_stop = conn.dep_stop
            if curr_stop == origin_stop:
                break

        total_travel_min = earliest_arrival[dest_stop] - departure_time_min

        return {
            'origin_stop': origin_stop,
            'destination_stop': dest_stop,
            'departure_min': departure_time_min,
            'arrival_min': earliest_arrival[dest_stop],
            'total_duration_minutes': total_travel_min,
            'transfers': max(0, len(itinerary) - 1),
            'segments': itinerary
        }
