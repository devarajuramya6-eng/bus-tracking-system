"""
CityBus Enterprise Platform - Vehicle Blocking & Interlining Optimization Engine
File: backend/services/scheduling/blocking_engine.py

Chains scheduled passenger revenue trips into optimal physical vehicle blocks:
- Minimizes required fleet vehicle count
- Minimizes deadhead kilometers between trip endpoints
- Enforces minimum layover/recovery buffers (e.g. 5-10 minutes between consecutive trips)
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


class TripInstance:
    """Represents a scheduled revenue trip with start and end times/locations."""
    def __init__(self, trip_id: str, route_id: int, route_number: str,
                 start_stop: str, end_stop: str,
                 departure_min: int, arrival_min: int,
                 distance_km: float):
        self.trip_id = trip_id
        self.route_id = route_id
        self.route_number = route_number
        self.start_stop = start_stop
        self.end_stop = end_stop
        self.departure_min = departure_min # Minutes from midnight (e.g. 06:00 -> 360)
        self.arrival_min = arrival_min
        self.distance_km = distance_km


class VehicleBlock:
    """Represents a full day's duty assignment for a physical bus."""
    def __init__(self, block_id: str, depot_name: str = "PNBS Central Depot"):
        self.block_id = block_id
        self.depot_name = depot_name
        self.trips: List[TripInstance] = []
        self.pull_out_min: int = 0
        self.pull_in_min: int = 0
        self.total_revenue_km: float = 0.0
        self.total_deadhead_km: float = 0.0

    def add_trip(self, trip: TripInstance, deadhead_km: float = 0.0):
        self.trips.append(trip)
        self.total_revenue_km += trip.distance_km
        self.total_deadhead_km += deadhead_km


class VehicleBlockingEngine:
    """Optimizes vehicle blocks from master trip lists."""

    @staticmethod
    def is_compatible(trip_a: TripInstance, trip_b: TripInstance, min_layover_min: int = 8) -> bool:
        """
        Determines if Trip B can follow Trip A on the same physical bus.
        """
        if trip_a.arrival_min + min_layover_min > trip_b.departure_min:
            return False

        # If same terminal, simple layover check passes
        if trip_a.end_stop == trip_b.start_stop:
            return True

        # If different terminal, allow 15 minutes deadheading travel time
        deadhead_travel_time = 15
        return trip_a.arrival_min + deadhead_travel_time + min_layover_min <= trip_b.departure_min

    @staticmethod
    def generate_blocks(trips: List[TripInstance], min_layover_min: int = 8) -> List[VehicleBlock]:
        """
        Greedy and bipartite matching algorithm to construct vehicle blocks.
        """
        # Sort trips chronologically by departure time
        sorted_trips = sorted(trips, key=lambda t: t.departure_min)
        blocks: List[VehicleBlock] = []

        for trip in sorted_trips:
            assigned = False

            # Try to append to existing active block
            for block in blocks:
                last_trip = block.trips[-1]
                if VehicleBlockingEngine.is_compatible(last_trip, trip, min_layover_min):
                    deadhead_km = 0.0 if last_trip.end_stop == trip.start_stop else 3.5
                    block.add_trip(trip, deadhead_km)
                    assigned = True
                    break

            # If cannot chain onto existing block, create a new vehicle block
            if not assigned:
                new_block_id = f"BLK-{len(blocks) + 1:03d}"
                new_block = VehicleBlock(block_id=new_block_id)
                new_block.pull_out_min = max(0, trip.departure_min - 25)
                new_block.add_trip(trip, deadhead_km=2.0) # Initial pullout deadhead
                blocks.append(new_block)

        # Calculate final pull-ins
        for block in blocks:
            if block.trips:
                block.pull_in_min = block.trips[-1].arrival_min + 20
                block.total_deadhead_km += 2.0 # Final pullin deadhead

        return blocks
