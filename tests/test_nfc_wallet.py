"""
CityBus Enterprise Platform - NFC Digital Wallet & HCE Tests
File: tests/test_nfc_wallet.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.nfc_wallet.hce_transit_token_service import HCETokenizationService
from services.nfc_wallet.offline_nfc_tap_authorizer import NFCTapAuthorizer
from services.nfc_wallet.auto_topup_ach_trigger import AutoTopupACHTrigger


class TestNFCWallet(unittest.TestCase):
    def test_hce_digital_pass_provisioning(self):
        pass_data = HCETokenizationService.provision_digital_pass(
            user_id=101,
            original_card_id="CARD_123456",
            device_id="PIXEL_7_PRO_01"
        )
        self.assertTrue(pass_data['express_transit_mode_enabled'])
        self.assertTrue(pass_data['device_account_number_dpan'].startswith('4900'))
        self.assertEqual(pass_data['token_state'], 'ACTIVE_PROVISIONED')

    def test_nfc_tap_authorizer_success(self):
        tap = NFCTapAuthorizer.process_nfc_tap(
            dpan_token="4900AABBCCDDEEFF",
            balance_inr=150.0,
            fare_inr=25.0
        )
        self.assertTrue(tap['authorized'])
        self.assertEqual(tap['remaining_balance_inr'], 125.0)
        self.assertEqual(tap['gate_action'], 'OPEN_TURNSTILE_BARRIER')
        self.assertLess(tap['execution_time_ms'], 150)

    def test_nfc_tap_authorizer_insufficient_funds(self):
        tap = NFCTapAuthorizer.process_nfc_tap(
            dpan_token="4900AABBCCDDEEFF",
            balance_inr=10.0,
            fare_inr=25.0
        )
        self.assertFalse(tap['authorized'])
        self.assertEqual(tap['error'], 'INSUFFICIENT_PURSE_BALANCE')

    def test_auto_topup_trigger(self):
        reload = AutoTopupACHTrigger.evaluate_auto_topup(
            user_id=101,
            current_balance_inr=25.0, # < 50 INR
            auto_topup_enabled=True,
            reload_amount_inr=200.0
        )
        self.assertTrue(reload['is_mandate_executed'])
        self.assertEqual(reload['updated_balance_inr'], 225.0)
        self.assertEqual(reload['payment_rail'], 'UPI_AUTOPAY_E_MANDATE')


if __name__ == '__main__':
    unittest.main()
