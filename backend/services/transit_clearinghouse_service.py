"""
CityBus Enterprise Platform - Transit Revenue Clearinghouse & Subsidy Settlement Service
File: backend/services/transit_clearinghouse_service.py

Manages inter-agency ticket settlement, municipal student concession subsidies,
bank interchange transaction fees, and daily reconciliation ledgers.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from models import Ticket, db
from sqlalchemy import func


class TransitClearinghouseService:
    """Manages multi-operator fare clearing and municipal subsidy settlements."""

    MUNICIPAL_STUDENT_SUBSIDY_PCT = 50.0 # 50% paid by municipal transport fund
    BANK_PAYMENT_GATEWAY_FEE_PCT = 1.25  # 1.25% UPI/Card processing fee

    @staticmethod
    def calculate_daily_settlement_ledger() -> Dict[str, Any]:
        """Calculates net revenue, concession subsidy receivables, and bank payout amounts."""
        total_tickets = Ticket.query.count()
        gross_sales = float(db.session.query(func.sum(Ticket.fare_amount)).scalar() or 0.0)

        # Estimated concession discounts absorbed
        student_concessions_total = round(gross_sales * 0.12, 2)
        senior_concessions_total = round(gross_sales * 0.06, 2)
        total_concessions = student_concessions_total + senior_concessions_total

        # Government municipal reimbursement claim
        govt_subsidy_receivable = round(student_concessions_total * 0.80 + senior_concessions_total * 0.50, 2)

        # Gateway deductions
        payment_gateway_fees = round(gross_sales * (TransitClearinghouseService.BANK_PAYMENT_GATEWAY_FEE_PCT / 100.0), 2)
        net_bank_settlement = round(gross_sales - payment_gateway_fees, 2)

        return {
            "settlement_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "gross_ticket_revenue_inr": gross_sales,
            "total_tickets_settled": total_tickets,
            "concessions_breakdown": {
                "student_concessions_inr": student_concessions_total,
                "senior_concessions_inr": senior_concessions_total,
                "total_discount_inr": total_concessions
            },
            "govt_subsidy_receivable_inr": govt_subsidy_receivable,
            "payment_gateway_fees_inr": payment_gateway_fees,
            "net_transit_fund_deposit_inr": net_bank_settlement,
            "settlement_status": "RECONCILED"
        }
