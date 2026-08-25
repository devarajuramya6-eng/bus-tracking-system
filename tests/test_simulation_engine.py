"""
CityBus Enterprise Platform - Simulation Engine Unit Tests
File: tests/test_simulation_engine.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.simulation.multi_route_simulator import MultiRouteSimulator, SimulatedBusState
from services.simulation.traffic_congestion_injector import CongestionInjector


class TestSimulationEngine(unittest.TestCase):
    def test_multi_route_simulator_tick(self):
        bus1 = SimulatedBusState(bus_id=1, bus_number="AP16-001", route_id=1, waypoints=[[16.5100, 80.6175], [16.5020, 80.6475]])
        sim = MultiRouteSimulator([bus1])

        updates = sim.tick_simulation(dt_seconds=1.0, speed_multiplier=1.0)
        self.assertEqual(len(updates), 1)
        self.assertEqual(updates[0]['bus_id'], 1)
        self.assertIn('latitude', updates[0])
        self.assertIn('longitude', updates[0])

    def test_traffic_congestion_injection(self):
        # Coordinates at Benz Circle Flyover (Hotspot)
        speed = CongestionInjector.adjust_speed_for_congestion(lat=16.5020, lng=80.6475, nominal_speed_kmh=40.0)
        self.assertLess(speed, 40.0)


if __name__ == '__main__':
    unittest.main()
