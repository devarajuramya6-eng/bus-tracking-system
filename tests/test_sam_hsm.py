"""
CityBus Enterprise Platform - SAM HSM & Contactless Payment Tests
File: tests/test_sam_hsm.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.sam_hsm.desfire_ev3_crypto_engine import DESFireEV3CryptoEngine
from services.sam_hsm.emv_offline_data_authentication import EMVOfflineDataAuthenticator
from services.sam_hsm.clearinghouse_settlement_batch import ClearinghouseSettlementBatch


class TestSAMHSM(unittest.TestCase):
    def test_desfire_ev3_cryptogram_generation(self):
        tap = DESFireEV3CryptoEngine.generate_tap_cryptogram(
            card_uid="04A1B2C3D4",
            card_nonce="8A7B6C5D",
            validator_nonce="1E2F3A4B",
            purse_balance_inr=150.0,
            fare_debited_inr=25.0
        )
        self.assertEqual(tap['post_tap_balance_inr'], 125.0)
        self.assertTrue(tap['is_tamper_proof'])
        self.assertEqual(len(tap['sam_cryptogram_cmac']), 16)

    def test_emv_contactless_cda_offline_approval(self):
        emv = EMVOfflineDataAuthenticator.verify_emv_contactless_tap(
            pan_masked="4532XXXXXXXX1289",
            amount_inr=35.0, # Below 2000 INR
            atc_counter=14,
            arqc_hex="A1B2C3D4E5F6"
        )
        self.assertEqual(emv['oda_result'], 'CDA_AUTHENTICATED_OFFLINE')
        self.assertEqual(emv['terminal_action'], 'APPROVE_GATE_UNLOCK')

    def test_clearinghouse_settlement_batch(self):
        txs = [{'amount_inr': 20.0}, {'amount_inr': 30.0}, {'amount_inr': 50.0}] # Total 100
        batch = ClearinghouseSettlementBatch.generate_settlement_batch(txs)
        self.assertEqual(batch['gross_fare_collection_inr'], 100.0)
        self.assertEqual(batch['bank_mdr_fee_inr'], 0.45) # 0.45%
        self.assertEqual(batch['net_municipal_remittance_inr'], 99.55)


if __name__ == '__main__':
    unittest.main()
