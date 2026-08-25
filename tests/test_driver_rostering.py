"""
CityBus Enterprise Platform - Driver Rostering & Union Regulations Tests
File: tests/test_driver_rostering.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.driver_rostering.union_shift_rules_enforcer import UnionShiftRulesEnforcer
from services.driver_rostering.leave_bidding_and_swapping import DriverShiftSwapManager
from services.driver_rostering.shift_fairness_gini_coefficient import ShiftFairnessGiniCalculator


class TestDriverRostering(unittest.TestCase):
    def test_union_shift_rules_valid(self):
        val = UnionShiftRulesEnforcer.validate_shift_assignment(
            scheduled_drive_hours=7.5,
            continuous_wheel_hours=3.5,
            rest_since_last_shift_hours=13.0
        )
        self.assertTrue(val['is_labor_compliant'])
        self.assertEqual(val['duty_authorization'], 'AUTHORIZED_FOR_DUTY')

    def test_union_shift_rules_violation(self):
        val = UnionShiftRulesEnforcer.validate_shift_assignment(
            scheduled_drive_hours=9.5, # > 8.0h limit
            continuous_wheel_hours=4.5, # > 4.0h limit
            rest_since_last_shift_hours=9.0  # < 11.0h limit
        )
        self.assertFalse(val['is_labor_compliant'])
        self.assertEqual(val['violations_count'], 3)

    def test_peer_shift_swap_approval(self):
        swap = DriverShiftSwapManager.process_peer_swap(
            driver_a_id=1, driver_a_hours=32.0,
            driver_b_id=2, driver_b_hours=38.0,
            target_shift_hours=8.0 # A becomes 40h (<=48h), B becomes 30h
        )
        self.assertTrue(swap['is_swap_authorized'])
        self.assertEqual(swap['status'], 'SWAP_APPROVED_BY_DISPATCH')

    def test_shift_fairness_gini_coefficient(self):
        hours = [38.0, 40.0, 39.0, 41.0, 40.0]
        res = ShiftFairnessGiniCalculator.calculate_workload_gini(hours)
        self.assertLess(res['gini_coefficient'], 0.10)
        self.assertTrue(res['is_equitable'])


if __name__ == '__main__':
    unittest.main()
