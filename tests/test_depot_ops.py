"""
CityBus Enterprise Platform - Depot Operations & Logistics Unit Tests
File: tests/test_depot_ops.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.depot_ops.bay_parking_optimizer import DepotParkingOptimizer
from services.depot_ops.daily_dispatch_roster import DailyDispatchRosterManager
from services.depot_ops.fuel_bowser_automation import FuelBowserAutomationEngine


class TestDepotOperations(unittest.TestCase):
    def test_depot_yard_parking_optimization(self):
        fleet = [
            {'bus_id': 1, 'is_electric': True, 'pullout_time_min': 330},
            {'bus_id': 2, 'is_electric': True, 'pullout_time_min': 360},
            {'bus_id': 3, 'is_electric': False, 'pullout_time_min': 300},
            {'bus_id': 4, 'is_electric': False, 'pullout_time_min': 345}
        ]
        yard = DepotParkingOptimizer.optimize_yard_parking(fleet, num_lanes=4, lane_capacity=4)
        self.assertGreater(yard['total_lanes'], 0)
        self.assertEqual(yard['total_parked_buses'], 4)

    def test_daily_dispatch_roster(self):
        drivers = [
            {'id': 1, 'name': 'Ravi Kumar', 'status': 'Active', 'medical_fitness_valid': True},
            {'id': 2, 'name': 'Suresh Reddy', 'status': 'Active', 'medical_fitness_valid': True}
        ]
        duties = [
            {'duty_id': 'DUTY-01', 'route_number': '27A', 'sign_on': '05:30'},
            {'duty_id': 'DUTY-02', 'route_number': '5K', 'sign_on': '06:00'}
        ]
        roster = DailyDispatchRosterManager.build_daily_roster(drivers, duties)
        self.assertEqual(roster['filled_duties'], 2)
        self.assertEqual(roster['roster_coverage_pct'], 100.0)

    def test_fuel_bowser_dispensing(self):
        fuel_log = FuelBowserAutomationEngine.authorize_and_log_dispense(
            nozzle_id="NZ-01",
            bus_rfid_tag="TAG-AP16-001",
            bus_id=1,
            bus_number="AP16-001",
            liters_dispensed=45.0,
            odometer_km=14200.0,
            prev_odometer_km=14020.0 # 180 km / 45 L = 4.0 km/L
        )
        self.assertEqual(fuel_log['km_per_liter_economy'], 4.0)
        self.assertFalse(fuel_log['is_abnormal_consumption'])
        self.assertEqual(fuel_log['status'], 'DISPENSE_COMPLETED')


if __name__ == '__main__':
    unittest.main()
