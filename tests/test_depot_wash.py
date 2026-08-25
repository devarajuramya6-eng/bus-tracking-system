"""
CityBus Enterprise Platform - Depot Bus Wash & Undercarriage Scanner Tests
File: tests/test_depot_wash.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.depot_wash.undercarriage_camera_inspector import UndercarriageInspectionScanner
from services.depot_wash.water_recycling_filtration_telemetry import WashWaterRecyclingTelemetry
from services.depot_wash.automated_wash_cycle_scheduler import BusWashCycleScheduler


class TestDepotWash(unittest.TestCase):
    def test_undercarriage_inspection_pass(self):
        scan = UndercarriageInspectionScanner.audit_chassis_imagery(
            bus_number="AP16-001",
            detected_leaks_count=0,
            structural_defects_count=0,
            corrosion_index_pct=5.0
        )
        self.assertTrue(scan['is_vehicle_cleared_for_service'])
        self.assertEqual(scan['inspection_result'], 'PASS_CHASSIS_CLEARED')

    def test_undercarriage_critical_defect(self):
        scan = UndercarriageInspectionScanner.audit_chassis_imagery(
            bus_number="AP16-014",
            detected_leaks_count=2,
            structural_defects_count=1,
            corrosion_index_pct=25.0
        )
        self.assertFalse(scan['is_vehicle_cleared_for_service'])
        self.assertEqual(scan['inspection_result'], 'GROUND_VEHICLE_CRITICAL_CHASSIS_DEFECT')

    def test_wash_water_recycling_compliance(self):
        water = WashWaterRecyclingTelemetry.evaluate_water_quality(tss_mg_l=30.0, ph_level=7.2, recycled_flow_lpm=140.0)
        self.assertTrue(water['is_water_quality_compliant'])
        self.assertEqual(water['status'], 'RECYCLING_PLANT_NOMINAL')

    def test_bus_wash_cycle_scheduling(self):
        sched = BusWashCycleScheduler.audit_bus_hygiene(bus_number="AP16-001", days_since_exterior_wash=2, days_since_interior_deep_clean=8)
        self.assertEqual(sched['assigned_wash_bay'], 'BAY_2_DEEP_CLEAN_AND_MISTING')


if __name__ == '__main__':
    unittest.main()
