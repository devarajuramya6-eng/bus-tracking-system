"""
CityBus Enterprise Platform - Driver Wellness & Interlock Unit Tests
File: tests/test_driver_wellness.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.driver_wellness.alcohol_interlock_telemetry import AlcoholInterlockVerifier
from services.driver_wellness.ergonomic_vibration_index import ErgonomicVibrationMonitor
from services.driver_wellness.duty_fairness_optimizer import DriverRosterFairnessOptimizer


class TestDriverWellness(unittest.TestCase):
    def test_breathalyzer_pass(self):
        res = AlcoholInterlockVerifier.verify_breath_sample(
            driver_id=10,
            driver_name="Ramesh",
            bus_id=1,
            measured_bac_percent=0.000
        )
        self.assertTrue(res['test_passed'])
        self.assertTrue(res['ignition_relay_authorized'])
        self.assertEqual(res['interlock_status'], 'IGNITION_UNLOCKED')

    def test_breathalyzer_fail(self):
        res = AlcoholInterlockVerifier.verify_breath_sample(
            driver_id=10,
            driver_name="Ramesh",
            bus_id=1,
            measured_bac_percent=0.045
        )
        self.assertFalse(res['test_passed'])
        self.assertFalse(res['ignition_relay_authorized'])
        self.assertEqual(res['interlock_status'], 'ENGINE_CRANK_LOCKOUT_TRIGGERED')

    def test_ergonomic_vibration_eav(self):
        accel_samples = [1.2, 1.4, 1.8, 1.5] * 20
        res = ErgonomicVibrationMonitor.calculate_vdv(accel_samples, dt_seconds=0.5)
        self.assertGreater(res['vdv_score'], 0.0)

    def test_duty_fairness_optimizer(self):
        workloads = [
            {'driver_id': 1, 'total_hours_week': 42.0},
            {'driver_id': 2, 'total_hours_week': 44.0},
            {'driver_id': 3, 'total_hours_week': 40.0}
        ]
        audit = DriverRosterFairnessOptimizer.audit_roster_fairness(workloads)
        self.assertEqual(audit['overworked_drivers_count'], 0)
        self.assertEqual(audit['compliance_status'], 'FAIR_AND_COMPLIANT')


if __name__ == '__main__':
    unittest.main()
