"""
CityBus Enterprise Platform - Automatic Fare Collection (AFC) & NCMC Tests
File: tests/test_afc.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.afc.validator_hardware_sim import ContactlessValidatorSimulator
from services.afc.ncmc_security_module import NCMCSecurityModule
from services.afc.offline_blacklist_manager import OfflineBlacklistManager
from services.afc.concession_document_ocr import ConcessionDocumentVerifier


class TestAutomaticFareCollection(unittest.TestCase):
    def test_contactless_validator_tap_approved(self):
        sim = ContactlessValidatorSimulator("ETV-TEST-01", bus_id=1)
        res = sim.process_tap(
            card_uid="NCMC-8849-2094",
            card_type="RUPAY_NCMC",
            current_balance=100.0,
            fare_amount=25.0,
            stop_name="Benz Circle",
            route_number="27A"
        )
        self.assertEqual(res['status'], 'APPROVED')
        self.assertEqual(res['remaining_balance'], 75.0)
        self.assertEqual(res['led_color'], 'GREEN')

    def test_contactless_validator_tap_declined(self):
        sim = ContactlessValidatorSimulator("ETV-TEST-01", bus_id=1)
        res = sim.process_tap(
            card_uid="NCMC-8849-2094",
            card_type="RUPAY_NCMC",
            current_balance=10.0,
            fare_amount=25.0,
            stop_name="Benz Circle",
            route_number="27A"
        )
        self.assertEqual(res['status'], 'DECLINED')
        self.assertEqual(res['led_color'], 'RED')

    def test_ncmc_sam_cryptogram_mac(self):
        mac_data = NCMCSecurityModule.generate_transaction_mac("CARD-1234", 1, 25.0, "2026-08-25T10:00:00")
        self.assertIn('cryptogram_mac', mac_data)
        self.assertTrue(mac_data['is_tamper_proof'])

        is_valid = NCMCSecurityModule.verify_transaction_mac("CARD-1234", 1, 25.0, "2026-08-25T10:00:00", mac_data['cryptogram_mac'])
        self.assertTrue(is_valid)

    def test_offline_blacklist(self):
        mgr = OfflineBlacklistManager()
        chk = mgr.is_card_blacklisted("CB-9988-1122-3344")
        self.assertTrue(chk['is_blacklisted'])
        self.assertEqual(chk['reason'], 'LOST_OR_STOLEN')

    def test_concession_document_verification(self):
        res = ConcessionDocumentVerifier.verify_student_document("Andhra Loyola College", "210482", 2027)
        self.assertTrue(res['is_eligible'])
        self.assertEqual(res['status'], 'APPROVED')


if __name__ == '__main__':
    unittest.main()
