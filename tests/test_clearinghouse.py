"""
CityBus Enterprise Platform - Clearinghouse & Accounting Unit Tests
File: tests/test_clearinghouse.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.clearinghouse.bank_settlement_reconciler import BankSettlementReconciler
from services.clearinghouse.conductor_cash_audit import ConductorCashAuditEngine
from services.clearinghouse.tax_gst_calculator import GSTTaxCalculator


class TestClearinghouseAndAccounting(unittest.TestCase):
    def test_bank_settlement_reconciler(self):
        internal_txs = [{'ref_id': 'TX-01', 'amount': 100.0}, {'ref_id': 'TX-02', 'amount': 50.0}]
        bank_file = [{'ref_id': 'TX-01', 'amount': 100.0}, {'ref_id': 'TX-02', 'amount': 50.0}]

        recon = BankSettlementReconciler.reconcile_batch(internal_txs, bank_file)
        self.assertEqual(recon['matched_count'], 2)
        self.assertEqual(recon['unmatched_count'], 0)
        self.assertEqual(recon['settlement_status'], 'CLEARED')
        self.assertGreater(recon['total_bank_fees_inr'], 0.0)

    def test_conductor_cash_audit_matched(self):
        audit = ConductorCashAuditEngine.audit_shift_remittance(
            conductor_id=401,
            conductor_name="K. Venkatesh",
            shift_id="SH-01",
            bus_number="AP16-001",
            etm_cash_total=4500.0,
            etm_digital_total=2500.0,
            physical_cash_handed_over=4500.0
        )
        self.assertEqual(audit['audit_status'], 'MATCHED')
        self.assertEqual(audit['variance_amount'], 0.0)

    def test_gst_tax_calculation(self):
        # 5% GST for AC Express
        gst = GSTTaxCalculator.calculate_gst(base_amount=100.0, service_type='AC_ELECTRIC_DELUXE')
        self.assertEqual(gst['gst_rate_pct'], 5)
        self.assertEqual(gst['total_gst_inr'], 5.0)
        self.assertEqual(gst['total_invoice_amount_inr'], 105.0)


if __name__ == '__main__':
    unittest.main()
