"""
CityBus Enterprise Platform - Scheduling & Blocking Unit Tests
File: tests/test_scheduling.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.scheduling.blocking_engine import VehicleBlockingEngine, TripInstance
from services.scheduling.runcutting_engine import CrewRuncuttingEngine
from services.scheduling.deadhead_calculator import DeadheadCalculator
from services.scheduling.timetable_generator import TimetableGenerator


class TestSchedulingEngine(unittest.TestCase):
    def test_vehicle_blocking(self):
        trips = [
            TripInstance("T1", 1, "27A", "PNBS", "Guntur", 360, 420, 32.0),
            TripInstance("T2", 1, "27A", "Guntur", "PNBS", 435, 495, 32.0),
            TripInstance("T3", 2, "5K", "PNBS", "Autonagar", 510, 550, 12.0)
        ]
        blocks = VehicleBlockingEngine.generate_blocks(trips, min_layover_min=10)
        self.assertGreater(len(blocks), 0)
        self.assertGreater(blocks[0].total_revenue_km, 0)

    def test_crew_runcutting(self):
        trips = [
            TripInstance("T1", 1, "27A", "PNBS", "Guntur", 360, 420, 32.0),
            TripInstance("T2", 1, "27A", "Guntur", "PNBS", 435, 495, 32.0)
        ]
        blocks = VehicleBlockingEngine.generate_blocks(trips)
        duties = CrewRuncuttingEngine.cut_duties(blocks)
        self.assertGreater(len(duties), 0)
        self.assertLessEqual(duties[0].driving_minutes, CrewRuncuttingEngine.MAX_DRIVING_MINUTES)

    def test_deadhead_cost_calculator(self):
        diesel_cost = DeadheadCalculator.calculate_cost(10.0, is_electric=False)
        self.assertEqual(diesel_cost['powertrain'], 'DIESEL')
        self.assertGreater(diesel_cost['cost_inr'], 0.0)

        ev_cost = DeadheadCalculator.calculate_cost(10.0, is_electric=True)
        self.assertEqual(ev_cost['powertrain'], 'ELECTRIC')
        self.assertGreater(ev_cost['cost_inr'], 0.0)

    def test_timetable_generator(self):
        stops = [{'id': 1, 'name': 'PNBS'}, {'id': 2, 'name': 'Benz Circle'}]
        timetable = TimetableGenerator.generate_corridor_timetable(1, "27A", stops, first_departure_min=360, last_departure_min=420, peak_headway_min=15)
        self.assertGreater(len(timetable), 1)
        self.assertEqual(timetable[0]['departure_time'], "06:00")


if __name__ == '__main__':
    unittest.main()
