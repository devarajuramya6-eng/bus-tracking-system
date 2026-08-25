"""
CityBus Enterprise Platform - Dynamic Fleet Sizing & Reserve Bus Allocator
File: backend/services/forecasting/dynamic_fleet_allocator.py

Calculates exact bus requirements per route based on hourly passenger demand:
- Peak hour bus frequency requirements (Headway min = (Bus Capacity * 60) / Demand per hour)
- Automated recommendation to inject standby buses from depot during unexpected demand spikes
"""

import math
from typing import List, Dict, Any


class DynamicFleetAllocator:
    BUS_CAPACITY = 45 # Standard 45-seater bus capacity

    @staticmethod
    def calculate_fleet_requirement(route_id: int, route_number: str,
                                    peak_hourly_demand: int,
                                    round_trip_duration_min: int) -> Dict[str, Any]:
        """
        Calculates optimal fleet count and headway to service passenger demand.
        """
        # Desired trips per hour to carry peak load
        trips_per_hour = math.ceil(peak_hourly_demand / float(DynamicFleetAllocator.BUS_CAPACITY))
        trips_per_hour = max(2, min(20, trips_per_hour)) # Clamp between 2 and 20 trips/hr

        headway_min = max(3, int(60.0 / trips_per_hour))
        
        # Number of buses required to maintain this frequency over round trip
        buses_needed = math.ceil(round_trip_duration_min / float(headway_min))

        return {
            'route_id': route_id,
            'route_number': route_number,
            'peak_hourly_demand': peak_hourly_demand,
            'round_trip_duration_min': round_trip_duration_min,
            'recommended_headway_min': headway_min,
            'required_operating_buses': buses_needed,
            'recommended_reserve_buses': max(1, int(buses_needed * 0.10)),
            'total_allocated_fleet': buses_needed + max(1, int(buses_needed * 0.10))
        }
