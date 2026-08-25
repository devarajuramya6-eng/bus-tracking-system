"""
CityBus Enterprise Platform - Conductor Daily Cash Audit & Waybill Reconciliation
File: backend/services/clearinghouse/conductor_cash_audit.py

Reconciles conductor physical cash bag remittance against POS terminal audit logs:
- Electronic Ticket Machine (ETM) issue counter verification
- Cash shortage / excess variance auditing
- Treasury remittance receipt generation
"""

from typing import Dict, Any
from datetime import datetime


class ConductorCashAuditEngine:
    @staticmethod
    def audit_shift_remittance(conductor_id: int, conductor_name: str,
                               shift_id: str, bus_number: str,
                               etm_cash_total: float,
                               etm_digital_total: float,
                               physical_cash_handed_over: float) -> Dict[str, Any]:
        """
        Performs end-of-shift cash bag audit.
        """
        variance = physical_cash_handed_over - etm_cash_total
        is_shortage = variance < -5.0 # Tolerance ₹5
        is_excess = variance > 5.0

        status = 'MATCHED'
        if is_shortage:
            status = 'SHORTAGE_DETECTED'
        elif is_excess:
            status = 'EXCESS_DEPOSITED'

        receipt_number = f"REMIT-VJA-{datetime.utcnow().strftime('%y%m%d%H%M')}-{conductor_id:03d}"

        return {
            'receipt_number': receipt_number,
            'conductor_id': conductor_id,
            'conductor_name': conductor_name,
            'shift_id': shift_id,
            'bus_number': bus_number,
            'etm_reported_cash': etm_cash_total,
            'etm_reported_digital': etm_digital_total,
            'total_shift_revenue': etm_cash_total + etm_digital_total,
            'physical_cash_deposited': physical_cash_handed_over,
            'variance_amount': round(variance, 2),
            'audit_status': status,
            'timestamp': datetime.utcnow().isoformat(),
            'requires_cashier_supervisor_signoff': is_shortage or is_excess
        }
