"""
CityBus Enterprise Platform - Fleet Asset Lifecycle & Overhaul Tests
File: tests/test_asset_lifecycle.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.asset_lifecycle.bus_straight_line_depreciation import FleetDepreciationCalculator
from services.asset_lifecycle.major_overhaul_milestone_tracker import OverhaulMilestoneTracker
from services.asset_lifecycle.procurement_rfp_evaluator import ProcurementRFPEvaluator


class TestAssetLifecycle(unittest.TestCase):
    def test_straight_line_depreciation(self):
        dep = FleetDepreciationCalculator.calculate_bus_asset_value(
            purchase_price_inr=3600000.0,
            age_years=6.0, # Halfway through 12-year life
            is_battery_pack=False
        )
        self.assertLess(dep['net_book_value_inr'], 3600000.0)
        self.assertGreater(dep['net_book_value_inr'], dep['salvage_value_inr'])
        self.assertFalse(dep['is_fully_depreciated'])

    def test_overhaul_milestone_detection(self):
        tracker = OverhaulMilestoneTracker.evaluate_bus_mileage("AP16-001", odometer_km=248500.0) # Close to 250k
        self.assertEqual(tracker['status'], 'OVERHAUL_WORK_ORDER_TRIGGERED')
        self.assertEqual(tracker['milestone_target_km'], 250000)

    def test_procurement_rfp_scoring(self):
        bids = [
            {'vendor_name': 'Vendor A (Low TCO)', 'tco_10yr_inr': 12000000.0, 'technical_score_100': 85.0},
            {'vendor_name': 'Vendor B (High TCO)', 'tco_10yr_inr': 18000000.0, 'technical_score_100': 90.0}
        ]
        scored = ProcurementRFPEvaluator.score_tender_bids(bids)
        self.assertEqual(len(scored), 2)
        self.assertEqual(scored[0]['vendor_name'], 'Vendor A (Low TCO)') # Highest composite


if __name__ == '__main__':
    unittest.main()
