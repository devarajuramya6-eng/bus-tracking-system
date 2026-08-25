"""
CityBus Enterprise Platform - Loyalty & Gamification Unit Tests
File: tests/test_loyalty.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.loyalty.commuter_pass_gamification import CommuterGamificationEngine
from services.loyalty.merchant_partner_discounts import MerchantDiscountPartnerEngine


class TestLoyaltyAndGamification(unittest.TestCase):
    def test_commuter_progress_evaluation(self):
        progress = CommuterGamificationEngine.evaluate_commuter_progress(
            user_id=1,
            total_trips=25,
            ev_trips=12,
            streak_days=5
        )
        self.assertEqual(progress['commuter_level'], 3)
        self.assertEqual(progress['tier_title'], 'SILVER_COMMUTER')
        self.assertGreater(len(progress['unlocked_badges']), 0)

    def test_merchant_partner_discounts(self):
        offers = MerchantDiscountPartnerEngine.get_available_offers("TKT-2026-0825-101")
        self.assertGreater(len(offers), 0)
        self.assertIn('coupon_code', offers[0])


if __name__ == '__main__':
    unittest.main()
