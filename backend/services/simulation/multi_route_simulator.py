"""
CityBus Enterprise Platform - Multi-Route Kinematic GPS Simulation Engine
File: backend/services/simulation/multi_route_simulator.py

Simulates realistic motion for 50 concurrent transit buses across 20 Vijayawada routes:
- Kinematic segment progression with stop dwell cycles (20-45 seconds at stops)
- Dynamic passenger boarding/alighting and seat occupancy fluctuation
- Speed modulation based on signal junctions and traffic congestion
"""

import math
import random
from typing import List, Dict, Any


class SimulatedBusState:
    def __init__(self, bus_id: int, bus_number: str, route_id: int, waypoints: List[List[float]], capacity: int = 45):
        self.bus_id = bus_id
        self.bus_number = bus_number
        self.route_id = route_id
        self.waypoints = waypoints or [[16.5062, 80.6480], [16.5100, 80.6175]]
        self.current_waypoint_idx = 0
        self.segment_progress = 0.0 # 0.0 to 1.0 along current segment
        self.speed_kmh = 35.0
        self.heading_deg = 90.0
        self.occupancy = random.randint(15, 38)
        self.capacity = capacity
        self.dwell_seconds_remaining = 0
        self.is_dwell = False


class MultiRouteSimulator:
    """Manages simultaneous kinematic simulation of the entire bus fleet."""

    def __init__(self, bus_states: List[SimulatedBusState] = None):
        self.buses = bus_states or []

    def add_bus(self, bus: SimulatedBusState):
        self.buses.append(bus)

    def tick_simulation(self, dt_seconds: float = 1.0, speed_multiplier: float = 1.0) -> List[Dict[str, Any]]:
        """
        Advances all buses by dt_seconds * speed_multiplier.
        """
        updates = []
        effective_dt = dt_seconds * speed_multiplier

        for bus in self.buses:
            # If bus is stopped at a station for passenger boarding
            if bus.is_dwell:
                bus.dwell_seconds_remaining -= effective_dt
                if bus.dwell_seconds_remaining <= 0:
                    bus.is_dwell = False
                    bus.speed_kmh = 32.0
                    # Passenger exchange
                    pax_alight = random.randint(1, min(8, bus.occupancy))
                    pax_board = random.randint(2, 9)
                    bus.occupancy = max(2, min(bus.capacity, bus.occupancy - pax_alight + pax_board))
                updates.append({
                    'bus_id': bus.bus_id,
                    'bus_number': bus.bus_number,
                    'latitude': bus.waypoints[bus.current_waypoint_idx][0],
                    'longitude': bus.waypoints[bus.current_waypoint_idx][1],
                    'speed_kmh': 0.0,
                    'heading_deg': bus.heading_deg,
                    'status': 'BOARDING_STOP',
                    'occupancy': bus.occupancy
                })
                continue

            # Advance along segment
            curr_pt = bus.waypoints[bus.current_waypoint_idx]
            next_idx = (bus.current_waypoint_idx + 1) % len(bus.waypoints)
            next_pt = bus.waypoints[next_idx]

            # Segment distance approx
            d_lat = next_pt[0] - curr_pt[0]
            d_lng = next_pt[1] - curr_pt[1]
            seg_dist_km = math.sqrt(d_lat*d_lat + d_lng*d_lng) * 111.0
            
            # Progress step
            speed_km_s = (bus.speed_kmh / 3600.0)
            step_progress = (speed_km_s * effective_dt) / max(0.01, seg_dist_km)
            bus.segment_progress += step_progress

            # If reached next waypoint
            if bus.segment_progress >= 1.0:
                bus.segment_progress = 0.0
                bus.current_waypoint_idx = next_idx
                # Trigger stop dwell
                bus.is_dwell = True
                bus.dwell_seconds_remaining = random.randint(20, 35)
                bus.speed_kmh = 0.0

            # Interpolate coordinates
            interp_lat = curr_pt[0] + (next_pt[0] - curr_pt[0]) * bus.segment_progress
            interp_lng = curr_pt[1] + (next_pt[1] - curr_pt[1]) * bus.segment_progress

            # Calculate heading angle
            angle_rad = math.atan2(next_pt[1] - curr_pt[1], next_pt[0] - curr_pt[0])
            bus.heading_deg = (math.degrees(angle_rad) + 360.0) % 360.0

            updates.append({
                'bus_id': bus.bus_id,
                'bus_number': bus.bus_number,
                'latitude': round(interp_lat, 6),
                'longitude': round(interp_lng, 6),
                'speed_kmh': round(bus.speed_kmh, 1),
                'heading_deg': round(bus.heading_deg, 1),
                'status': 'EN_ROUTE',
                'occupancy': bus.occupancy
            })

        return updates
