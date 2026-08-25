"""
CityBus Enterprise Platform - High-Fidelity Multi-Vehicle GPS Simulator Engine
File: backend/services/simulator_service.py
"""

import math
import random
from datetime import datetime
from models import db, Bus, Route


class MultiBusSimulator:
    """Simulates realistic kinematic progression of municipal buses along corridor waypoints."""

    def __init__(self):
        self.is_running = True
        self.step_ratio = 0.08
        self.dwell_counters = {} # bus_id -> remaining_dwell_ticks

    def step_simulation(self):
        """Advances all active buses along their route geometries."""
        buses = Bus.query.filter(Bus.status != 'Offline').all()
        updated_buses = []

        for bus in buses:
            if not bus.route_id:
                continue

            route = Route.query.get(bus.route_id)
            if not route:
                continue

            waypoints = route.get_waypoints()
            if not waypoints or len(waypoints) < 2:
                continue

            # Check if bus is currently dwelling at a stop
            if self.dwell_counters.get(bus.id, 0) > 0:
                self.dwell_counters[bus.id] -= 1
                bus.speed = 0.0
                bus.last_gps_update = datetime.utcnow()
                updated_buses.append(bus)
                continue

            # Determine closest waypoint index or progress to next
            closest_idx = 0
            min_dist = float('inf')
            for idx, pt in enumerate(waypoints):
                d = math.hypot(bus.latitude - pt[0], bus.longitude - pt[1])
                if d < min_dist:
                    min_dist = d
                    closest_idx = idx

            # Target next waypoint
            target_idx = (closest_idx + 1) % len(waypoints)
            target = waypoints[target_idx]

            # Smooth interpolation with minor sensor jitter
            bus.latitude += (target[0] - bus.latitude) * self.step_ratio + (random.random() - 0.5) * 0.0002
            bus.longitude += (target[1] - bus.longitude) * self.step_ratio + (random.random() - 0.5) * 0.0002

            # Calculate heading
            dLon = math.radians(target[1] - bus.longitude)
            y = math.sin(dLon) * math.cos(math.radians(target[0]))
            x = math.cos(math.radians(bus.latitude)) * math.sin(math.radians(target[0])) - \
                math.sin(math.radians(bus.latitude)) * math.cos(math.radians(target[0])) * math.cos(dLon)
            bus.heading = round((math.degrees(math.atan2(y, x)) + 360) % 360, 1)

            # Fluctuate speed realistically
            if bus.status == 'On Route':
                bus.speed = float(random.randint(28, 48))
            elif bus.status == 'Delayed':
                bus.speed = float(random.randint(12, 22))

            # If reached target waypoint, trigger occasional 15-second dwell
            if min_dist < 0.002 and random.random() > 0.65:
                self.dwell_counters[bus.id] = 4 # 4 ticks dwell

            bus.last_gps_update = datetime.utcnow()
            updated_buses.append(bus)

        db.session.commit()
        return [b.to_dict() for b in updated_buses]


# Global Singleton Simulator Instance
simulator_engine = MultiBusSimulator()
