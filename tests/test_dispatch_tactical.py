"""
CityBus Enterprise Platform - Tactical Dispatch & Emergency Response Unit Tests
File: tests/test_dispatch_tactical.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.dispatch.headway_regulator import DynamicHeadwayRegulator
from services.dispatch.bus_insertion_service import BusInsertionService
from services.dispatch.emergency_coordinator import EmergencyCoordinator


class TestTacticalDispatch(unittest.TestCase):
    def test_dynamic_headway_holding_strategy(self):
        # Scheduled 600s, actual ahead is 180s (< 40% -> severe bunching)
        strategy = DynamicHeadwayRegulator.calculate_regulation_strategy(
            scheduled_headway_sec=600,
            actual_headway_ahead_sec=180,
            actual_headway_behind_sec=700,
            current_stop_name="Benz Circle"
        )
        self.assertEqual(strategy['action_type'], 'HOLD_AT_STOP')
        self.assertGreater(strategy['hold_duration_seconds'], 0)

    def test_standby_bus_insertion(self):
        res = BusInsertionService.recommend_insertion(incident_lat=16.5020, incident_lng=80.6475, route_id=1)
        self.assertEqual(res['status'], 'STANDBY_DISPATCH_RECOMMENDED')
        self.assertIn('assigned_standby_vehicle', res)

    def test_emergency_response_coordination(self):
        protocol = EmergencyCoordinator.coordinate_emergency(
            incident_id=501,
            bus_number="AP16-101",
            lat=16.5062,
            lng=80.6480
        )
        self.assertEqual(protocol['protocol_level'], 'PRIORITY_1_RED_ALERT')
        self.assertEqual(len(protocol['agencies_notified']), 3)


if __name__ == '__main__':
    unittest.main()
