"""
CityBus Enterprise Platform - Fare Matrix & Passes Unit Tests
File: tests/test_fare_matrix.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.fare.multi_zone_matrix import MultiZoneFareMatrix
from services.fare.pass_manager import TransitPassManager
from services.fare.smart_card_ledger import SmartCardLedgerEngine


class TestFareMatrixAndPasses(unittest.TestCase):
    def test_multi_zone_fare_calculation(self):
        fare = MultiZoneFareMatrix.calculate_fare('ZONE_1_CORE', 'ZONE_2_SUBURB', distance_km=12.0, concession_type='general')
        self.assertGreater(fare['total_fare'], 20.0)

        # Student 50% discount
        student_fare = MultiZoneFareMatrix.calculate_fare('ZONE_1_CORE', 'ZONE_2_SUBURB', distance_km=12.0, concession_type='student')
        self.assertAlmostEqual(student_fare['total_fare'], fare['total_fare'] * 0.5, delta=1.0)

    def test_transit_pass_issuance(self):
        pass_data = TransitPassManager.issue_pass(user_id=101, pass_type='MONTHLY_COMMUTER', passenger_name='Anil Kumar')
        self.assertEqual(pass_data['status'], 'ACTIVE')
        self.assertIn('pass_number', pass_data)
        self.assertIn('qr_payload', pass_data)

    def test_smart_card_double_entry_ledger(self):
        entry = SmartCardLedgerEngine.record_transaction(
            card_number='CB-8849-2094-1029',
            current_balance=250.0,
            amount=-25.0,
            tx_type='FARE_DEBIT',
            ref_id='TX-101',
            desc='Fare deduction on Route 27A'
        )
        self.assertEqual(entry['new_balance'], 225.0)
        self.assertEqual(entry['status'], 'SETTLED')


if __name__ == '__main__':
    unittest.main()
