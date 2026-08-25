"""
CityBus Enterprise Platform - GTFS-Fares V2 & Interoperability Tests
File: tests/test_fares_v2_interop.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.interoperability.gtfs_fares_v2_builder import GTFSFaresV2Builder
from services.interoperability.inter_agency_roaming_clearing import InterAgencyRoamingClearing
from services.interoperability.unified_qr_mapper import UnifiedQRMapper


class TestGTFSFaresV2AndInterop(unittest.TestCase):
    def test_gtfs_fares_v2_dataset_generation(self):
        products = [{'id': 'PROD_01', 'name': 'Ordinary Fare', 'amount': 20.0}]
        dataset = GTFSFaresV2Builder.generate_fares_v2_dataset(products)
        self.assertIn('fare_products.txt', dataset)
        self.assertIn('PROD_01', dataset['fare_products.txt'])
        self.assertIn('fare_leg_rules.txt', dataset)

    def test_inter_agency_roaming_clearing(self):
        txs = [{'id': 1, 'amount': 100.0}, {'id': 2, 'amount': 200.0}] # Total 300
        settle = InterAgencyRoamingClearing.settle_roaming_batch("APSRTC", "TSRTC", txs)
        self.assertEqual(settle['gross_fare_inr'], 300.0)
        self.assertEqual(settle['clearinghouse_fee_inr'], 3.0) # 1%
        self.assertEqual(settle['net_transfer_payable_inr'], 297.0)

    def test_unified_qr_decoding(self):
        res1 = UnifiedQRMapper.decode_emv_transit_qr("00020101021226580014APSRTC")
        self.assertEqual(res1['format'], 'EMVCO_TRANSIT_QR')

        res2 = UnifiedQRMapper.decode_emv_transit_qr("upi://pay?pa=citybus@sbi")
        self.assertEqual(res2['format'], 'BHARAT_QR_TRANSIT_SPEC')


if __name__ == '__main__':
    unittest.main()
