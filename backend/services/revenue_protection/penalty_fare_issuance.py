"""
CityBus Enterprise Platform - Statutory Penalty Fare Notice Generator
File: backend/services/revenue_protection/penalty_fare_issuance.py

Generates statutory penalty notices for ticketless travel (Section 178 MVA 1988):
- ₹500 standard penalty fare + single journey fare
- Instant UPI QR code payment link & thermal notice receipt
"""

from typing import Dict, Any
from datetime import datetime


class PenaltyFareGenerator:
    STATUTORY_PENALTY_INR = 500.0

    @staticmethod
    def issue_penalty_notice(inspector_id: int, bus_number: str, route_number: str,
                             violator_name: str, violator_phone: str, standard_fare_inr: float = 25.0) -> Dict[str, Any]:
        """
        Generates electronic penalty fare slip.
        """
        notice_id = f"PENALTY-{datetime.utcnow().strftime('%y%m%d%H%M')}-{inspector_id:02d}"
        total_payable = PenaltyFareGenerator.STATUTORY_PENALTY_INR + standard_fare_inr

        return {
            'penalty_notice_id': notice_id,
            'statutory_act': 'Motor Vehicles Act 1988 (Section 178 - Ticketless Travel)',
            'inspector_id': inspector_id,
            'bus_number': bus_number,
            'route_number': route_number,
            'violator_name': violator_name,
            'violator_phone': violator_phone,
            'penalty_amount_inr': PenaltyFareGenerator.STATUTORY_PENALTY_INR,
            'fare_evaded_inr': standard_fare_inr,
            'total_payable_inr': total_payable,
            'upi_qr_string': f"upi://pay?pa=citybus.revenue@sbi&pn=CityBus%20Revenue&am={total_payable}&tr={notice_id}",
            'payment_status': 'PENDING_ON_THE_SPOT_COLLECTION',
            'issued_at': datetime.utcnow().isoformat()
        }
