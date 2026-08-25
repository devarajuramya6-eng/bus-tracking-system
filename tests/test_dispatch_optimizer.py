"""
CityBus Enterprise Platform - Dispatch & Deadhead Optimization Tests
File: tests/test_dispatch_optimizer.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.dispatch_optimizer.hungarian_depot_assignment import HungarianDepotAssigner
from services.dispatch_optimizer.driver_shift_relief_station_sync import DriverReliefSyncEngine
from services.dispatch_optimizer.emergency_spare_bus_insertion import StandbySpareBusManager


class TestDispatchOptimizer(unittest.TestCase):
    def test_hungarian_depot_deadhead_minimization(self):
        depot_buses = [
            {'bus_id': 1, 'bus_number': 'AP16-001', 'depot_name': 'Depot A', 'depot_lat': 16.5100, 'depot_lng': 80.6175},
            {'bus_id': 2, 'bus_number': 'AP16-002', 'depot_name': 'Depot B', 'depot_lat': 16.5000, 'depot_lng': 80.6500}
        ]
        routes = [
            {'route_id': 1, 'route_number': '27A', 'start_lat': 16.5105, 'start_lng': 80.6180},
            {'route_id': 2, 'route_number': '5K', 'start_lat': 16.5010, 'start_lng': 80.6510}
        ]
        res = HungarianDepotAssigner.assign_minimum_deadhead_buses(depot_buses, routes)
        self.assertEqual(res['total_routes_dispatched'], 2)
        self.assertLess(res['total_deadhead_km'], 5.0)

    def test_driver_relief_handover_plan(self):
        plan = DriverReliefSyncEngine.plan_relief_handover(
            bus_number="AP16-001",
            route_number="27A",
            relief_stop_name="PNBS Bay 4",
            incoming_driver_name="Ravi Kumar",
            relieving_driver_name="K. Satyam",
            estimated_arrival_time_min=45.0
        )
        self.assertEqual(plan['handover_status'], 'RELIEF_CREW_READY_AT_PLATFORM')
        self.assertIn('BREATHALYZER_INTERLOCK_TAP', plan['required_steps'])

    def test_standby_spare_bus_insertion(self):
        spares = [{'bus_id': 99, 'bus_number': 'SPARE-01'}]
        ins = StandbySpareBusManager.dispatch_spare_insertion(
            disabled_bus_number="AP16-004",
            route_number="27A",
            breakdown_stop_index=5,
            available_spares=spares
        )
        self.assertTrue(ins['success'])
        self.assertEqual(ins['replacement_bus_number'], 'SPARE-01')
        self.assertEqual(ins['insertion_stop_index'], 6)


if __name__ == '__main__':
    unittest.main()
