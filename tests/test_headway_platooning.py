"""
CityBus Enterprise Platform - Headway Regularization & Platooning Tests
File: tests/test_headway_platooning.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.headway_platooning.holding_strategy_controller import HeadwayHoldingController
from services.headway_platooning.virtual_platoon_sync import VirtualPlatoonSyncEngine
from services.headway_platooning.express_overtaking_coordinator import ExpressOvertakingCoordinator


class TestHeadwayPlatooning(unittest.TestCase):
    def test_headway_holding_anti_bunching(self):
        hold = HeadwayHoldingController.calculate_holding_dwell(
            forward_headway_min=3.0, # Catching up!
            backward_headway_min=12.0,
            target_headway_min=10.0
        )
        self.assertEqual(hold['dispatch_command'], 'HOLD_AT_STATION')
        self.assertTrue(hold['bunching_prevented'])
        self.assertGreater(hold['recommended_holding_seconds'], 20)

    def test_virtual_platoon_spacing_lock(self):
        platoon = VirtualPlatoonSyncEngine.calculate_platoon_spacing(
            lead_bus_speed_kmh=40.0,
            lead_bus_brake_decel_mps2=0.0,
            follower_speed_kmh=40.0,
            actual_distance_gap_m=17.0
        )
        self.assertEqual(platoon['platoon_control_command'], 'MAINTAIN_VIRTUAL_PLATOON_LOCK')
        self.assertTrue(platoon['is_platoon_locked'])

    def test_express_overtaking_authorization_safe(self):
        ot = ExpressOvertakingCoordinator.evaluate_overtake_clearance(
            express_bus_number="AP16-100E",
            local_bus_number="AP16-005",
            station_id="STATION_BENZ_CIRCLE",
            passing_lane_clear=True,
            local_bus_stationary=True
        )
        self.assertEqual(ot['overtake_authorization'], 'GREEN_BYPASS_AUTHORIZED')
        self.assertTrue(ot['is_passing_safe'])


if __name__ == '__main__':
    unittest.main()
