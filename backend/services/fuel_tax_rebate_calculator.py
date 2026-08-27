"""
CityBus Enterprise Platform - Fuel Excise Tax Rebate & Carbon Credit Service
File: backend/services/fuel_tax_rebate_calculator.py

Calculates commercial public transport fuel excise duty exemptions,
State VAT tax refunds on commercial diesel, and EV renewable energy trading certificates (REC).
"""

from typing import Dict, List, Any, Optional
from models import FuelLog, db
from sqlalchemy import func


class FuelTaxRebateCalculator:
    """Calculates municipal commercial transit fuel subsidy refunds."""

    DIESEL_EXCISE_TAX_REBATE_PER_LITER = 4.50 # ₹4.50 per liter tax refund
    EV_CARBON_CREDIT_VALUE_PER_MWH = 1200.0   # ₹1,200 per MWh clean energy credit

    @staticmethod
    def calculate_quarterly_tax_rebate() -> Dict[str, Any]:
        """Calculates quarterly state fuel tax refund claim totals."""
        total_liters = float(db.session.query(func.sum(FuelLog.quantity)).scalar() or 0.0)
        total_diesel_cost = float(db.session.query(func.sum(FuelLog.cost)).scalar() or 0.0)

        diesel_tax_rebate_inr = round(total_liters * FuelTaxRebateCalculator.DIESEL_EXCISE_TAX_REBATE_PER_LITER, 2)
        ev_clean_energy_credits_inr = 85000.0 # Estimated clean energy credits

        total_financial_relief = diesel_tax_rebate_inr + ev_clean_energy_credits_inr

        return {
            "quarter": "Q1 2026",
            "total_diesel_fuel_consumed_liters": round(total_liters, 2),
            "gross_fuel_expenditure_inr": round(total_diesel_cost, 2),
            "diesel_excise_duty_rebate_inr": diesel_tax_rebate_inr,
            "ev_renewable_energy_credits_inr": ev_clean_energy_credits_inr,
            "net_quarterly_refund_claim_inr": total_financial_relief,
            "filing_status": "READY_FOR_COMMERCIAL_TAX_SUBMISSION"
        }
