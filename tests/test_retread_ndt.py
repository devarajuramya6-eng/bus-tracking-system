"""
CityBus Enterprise Platform - Tire Retreading & Laser NDT Tests
File: tests/test_retread_ndt.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.retread_ndt.casing_shearography_analyzer import TireShearographyAnalyzer
from services.retread_ndt.tread_depth_laser_scanner import TreadDepthLaserScanner
from services.retread_ndt.retread_lifecycle_roi_model import RetreadLifecycleROIModel


class TestRetreadNDT(unittest.TestCase):
    def test_shearography_casing_approval(self):
        casing = TireShearographyAnalyzer.evaluate_casing_scan(
            tire_serial_number="MICH-295-8941",
            retread_count=1,
            anomaly_count=0,
            max_fringe_diameter_mm=0.0
        )
        self.assertTrue(casing['procure_approval'])
        self.assertEqual(casing['casing_decision'], 'APPROVE_FOR_PRECURED_RETREADING')

    def test_shearography_casing_rejection(self):
        casing = TireShearographyAnalyzer.evaluate_casing_scan(
            tire_serial_number="APOL-295-3210",
            retread_count=1,
            anomaly_count=2, # Ply separation defect
            max_fringe_diameter_mm=14.0
        )
        self.assertFalse(casing['procure_approval'])
        self.assertEqual(casing['casing_decision'], 'REJECT_CASING_INTERNAL_PLY_SEPARATION')

    def test_drive_over_laser_tread_depth(self):
        scan = TreadDepthLaserScanner.process_drive_over_scan(
            bus_number="AP16-001",
            tire_readings=[
                {'position': 'STEER_LEFT', 'tread_depth_mm': 12.0},
                {'position': 'DRIVE_OUTER_RIGHT', 'tread_depth_mm': 2.5} # Below 3mm retread threshold
            ]
        )
        self.assertEqual(scan['tires_requiring_action'], 1)
        self.assertTrue(scan['is_fleet_safe_for_service'])

    def test_retread_lifecycle_cpkm_savings(self):
        roi = RetreadLifecycleROIModel.calculate_casing_lifecycle_cpkm(retread_count=2)
        self.assertGreater(roi['operating_cost_savings_pct'], 40.0)
        self.assertLess(roi['lifecycle_cpkm_inr'], roi['baseline_new_tire_cpkm_inr'])


if __name__ == '__main__':
    unittest.main()
