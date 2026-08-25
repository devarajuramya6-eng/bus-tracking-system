"""
CityBus Enterprise Platform - Fare Capping & Best-Price Tests
File: tests/test_fare_capping.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.fare_capping.daily_weekly_capping_engine import FareCappingEngine
from services.fare_capping.off_peak_concession_evaluator import ConcessionFareEvaluator
from services.fare_capping.group_family_ticket_bundler import GroupTicketBundler


class TestFareCapping(unittest.TestCase):
    def test_daily_fare_capping_reach_cap(self):
        # Already spent 60 INR today, standard fare is 25 INR, daily cap is 75 INR.
        # Should debit only 15 INR and save 10 INR!
        cap = FareCappingEngine.calculate_capped_fare(
            standard_fare_inr=25.0,
            accumulated_today_inr=60.0,
            accumulated_week_inr=150.0
        )
        self.assertEqual(cap['actual_fare_debited_inr'], 15.0)
        self.assertEqual(cap['commuter_savings_inr'], 10.0)
        self.assertEqual(cap['new_accumulated_today_inr'], 75.0)
        self.assertTrue(cap['is_daily_capped'])

    def test_free_ride_after_daily_cap_exceeded(self):
        cap = FareCappingEngine.calculate_capped_fare(
            standard_fare_inr=25.0,
            accumulated_today_inr=75.0, # Cap already met
            accumulated_week_inr=200.0
        )
        self.assertEqual(cap['actual_fare_debited_inr'], 0.0)
        self.assertEqual(cap['commuter_savings_inr'], 25.0)
        self.assertEqual(cap['status'], 'FREE_RIDE_FARE_CAPPED')

    def test_senior_citizen_concession(self):
        conc = ConcessionFareEvaluator.calculate_concession_fare(
            base_fare_inr=30.0,
            passenger_category="SENIOR_CITIZEN"
        )
        self.assertEqual(conc['final_payable_fare_inr'], 15.0) # 50% discount
        self.assertTrue(conc['is_concession_applied'])

    def test_family_group_ticket_bundling(self):
        bundle = GroupTicketBundler.bundle_group_pass(
            passenger_count=4,
            individual_fare_inr=25.0
        )
        self.assertEqual(bundle['gross_fare_inr'], 100.0)
        self.assertEqual(bundle['group_discount_inr'], 20.0) # 20% group discount
        self.assertEqual(bundle['net_bundle_fare_inr'], 80.0)
        self.assertTrue(bundle['is_group_discount_applied'])


if __name__ == '__main__':
    unittest.main()
