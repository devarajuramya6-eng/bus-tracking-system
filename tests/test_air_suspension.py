"""
CityBus Enterprise Platform - Air Suspension & ELC Kneeling Tests
File: tests/test_air_suspension.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.air_suspension.pneumatic_kneeling_controller import ElectronicLevelingController
from services.air_suspension.curb_distance_ultrasonic_aligner import CurbUltrasonicAligner
from services.air_suspension.axle_weight_distribution_balancer import AxleWeightBalancer


class TestAirSuspension(unittest.TestCase):
    def test_kneeling_command_stationary_valid(self):
        res = ElectronicLevelingController.execute_kneeling_command(
            command="KNEEL_RIGHT_DOORWAY",
            vehicle_speed_kmh=0.0,
            is_handbrake_engaged=True
        )
        self.assertTrue(res['success'])
        self.assertTrue(res['is_kneeled'])
        self.assertEqual(res['current_height_mm'], 270.0)

    def test_kneeling_command_blocked_while_moving(self):
        res = ElectronicLevelingController.execute_kneeling_command(
            command="KNEEL_RIGHT_DOORWAY",
            vehicle_speed_kmh=12.0, # Moving
            is_handbrake_engaged=False
        )
        self.assertFalse(res['success'])
        self.assertFalse(res['is_kneeled'])

    def test_curb_ultrasonic_alignment_perfect(self):
        gap = CurbUltrasonicAligner.evaluate_docking_gap(lateral_curb_distance_mm=45.0)
        self.assertTrue(gap['is_step_free_accessible'])
        self.assertEqual(gap['docking_alignment_status'], 'PERFECT_KASSEL_DOCK_STEP_FREE')

    def test_axle_weight_distribution_balancing(self):
        bal = AxleWeightBalancer.balance_suspension_pressures(
            steer_left_bar=6.8, steer_right_bar=6.7,
            drive_left_bar=6.9, drive_right_bar=6.8,
            lateral_accel_g=0.05
        )
        self.assertTrue(bal['is_chassis_level'])


if __name__ == '__main__':
    unittest.main()
