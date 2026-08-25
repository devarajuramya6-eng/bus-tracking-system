"""
CityBus Enterprise Platform - NPCI NCMC & Acquiring Bank Settlement Reconciler
File: backend/services/clearinghouse/bank_settlement_reconciler.py

Reconciles daily electronic transit transactions with banking network clearing files:
- NPCI RuPay NCMC Clearing & Settlement (NCS) processing
- Merchant Discount Rate (MDR 1.15%) and interchange fee calculations
- Unmatched transaction exception isolation
"""

from typing import List, Dict, Any
from datetime import datetime


class BankSettlementReconciler:
    MDR_PERCENTAGE = 0.0115 # 1.15% Acquiring Bank fee
    GST_ON_MDR_PERCENTAGE = 0.18 # 18% GST on MDR

    @staticmethod
    def reconcile_batch(internal_transactions: List[Dict[str, Any]], bank_settlement_file: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Matches internal ETV records against bank clearing house logs.
        """
        bank_tx_map = {b['ref_id']: b for b in bank_settlement_file}

        matched_txs = []
        unmatched_internal = []
        gross_volume = 0.0
        total_mdr_fee = 0.0

        for tx in internal_transactions:
            ref = tx.get('ref_id')
            amount = tx.get('amount', 0.0)
            gross_volume += amount

            if ref in bank_tx_map:
                bank_record = bank_tx_map[ref]
                mdr = amount * BankSettlementReconciler.MDR_PERCENTAGE
                gst = mdr * BankSettlementReconciler.GST_ON_MDR_PERCENTAGE
                net_payout = amount - mdr - gst
                total_mdr_fee += (mdr + gst)

                matched_txs.append({
                    'ref_id': ref,
                    'gross_amount': amount,
                    'mdr_fee': round(mdr, 2),
                    'gst_on_fee': round(gst, 2),
                    'net_settlement': round(net_payout, 2),
                    'status': 'RECONCILED'
                })
            else:
                unmatched_internal.append(tx)

        net_settled_amount = gross_volume - total_mdr_fee

        return {
            'reconciliation_date': datetime.utcnow().strftime('%Y-%m-%d'),
            'total_internal_transactions': len(internal_transactions),
            'matched_count': len(matched_txs),
            'unmatched_count': len(unmatched_internal),
            'gross_volume_inr': round(gross_volume, 2),
            'total_bank_fees_inr': round(total_mdr_fee, 2),
            'net_settled_payout_inr': round(net_settled_amount, 2),
            'settlement_status': 'CLEARED' if len(unmatched_internal) == 0 else 'DISCREPANCY_FLAGGED',
            'matched_records': matched_txs,
            'unmatched_records': unmatched_internal
        }
