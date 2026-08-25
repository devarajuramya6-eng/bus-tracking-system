"""
CityBus Enterprise Platform - Revenue Protection & Fare Evasion Tests
File: tests/test_revenue_protection.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.revenue_protection.fare_evasion_classifier import FareEvasionClassifier
from services.revenue_protection.ticket_inspector_roster import TicketInspectorRosterManager
from services.revenue_protection.penalty_fare_issuance import PenaltyFareGenerator


class TestRevenueProtection(unittest.TestCase):
    def test_fare_evasion_classification(self):
        res = FareEvasionClassifier.evaluate_stop_segment(
            stop_id=1,
            stop_name="Ramavarappadu Ring",
            apc_boardings=40,
            ticket_validations=28 # 12 unvalidated (30%)
        )
        self.assertEqual(res['unvalidated_passengers'], 12)
        self.assertEqual(res['risk_level'], 'HIGH_REVENUE_LEAKAGE')
        self.assertTrue(res['inspector_dispatch_recommended'])

    def test_inspector_roster_planning(self):
        inspectors = [{'id': 1, 'name': 'V. Rao'}, {'id': 2, 'name': 'K. Suresh'}]
        corridors = ['Route 5K', 'Route 27A']
        assignments = TicketInspectorRosterManager.plan_inspector_shifts(inspectors, corridors)
        self.assertEqual(len(assignments), 2)
        self.assertEqual(assignments[0]['target_corridor'], 'Route 5K')

    def test_penalty_fare_notice_generation(self):
        notice = PenaltyFareGenerator.issue_penalty_notice(
            inspector_id=1,
            bus_number="AP16-004",
            route_number="5K",
            violator_name="G. Rajesh",
            violator_phone="9876543210",
            standard_fare_inr=20.0
        )
        self.assertEqual(notice['total_payable_inr'], 520.0)
        self.assertIn('upi://pay', notice['upi_qr_string'])


if __name__ == '__main__':
    unittest.main()
