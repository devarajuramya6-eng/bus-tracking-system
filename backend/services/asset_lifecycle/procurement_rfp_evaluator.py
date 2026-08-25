"""
CityBus Enterprise Platform - Municipal EV Bus Procurement RFP Bid Scoring Engine
File: backend/services/asset_lifecycle/procurement_rfp_evaluator.py

Evaluates manufacturer tender bids using Quality & Cost-Based Selection (QCBS):
- 70% Financial Weighting: 10-Year Total Cost of Ownership (CapEx + Energy + Maintenance)
- 30% Technical Weighting: Battery warranty, range per charge, localized AIS-052 body code compliance
"""

from typing import List, Dict, Any


class ProcurementRFPEvaluator:
    @staticmethod
    def score_tender_bids(bids: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculates QCBS composite scores for tender evaluation.
        """
        if not bids:
            return []

        min_tco = min(b.get('tco_10yr_inr', float('inf')) for b in bids)

        evaluated = []
        for b in bids:
            tco = b.get('tco_10yr_inr', 1.0)
            tech_score = b.get('technical_score_100', 80.0)

            # Financial score = (Min_TCO / Bid_TCO) * 70
            financial_score = (min_tco / max(1.0, tco)) * 70.0
            technical_weighted = (tech_score / 100.0) * 30.0
            composite_score = financial_score + technical_weighted

            evaluated.append({
                'vendor_name': b.get('vendor_name', 'Unknown'),
                'tco_10yr_inr': round(tco, 2),
                'financial_score_70': round(financial_score, 2),
                'technical_score_30': round(technical_weighted, 2),
                'composite_score_100': round(composite_score, 2)
            })

        return sorted(evaluated, key=lambda x: x['composite_score_100'], reverse=True)
