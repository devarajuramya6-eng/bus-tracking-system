"""
CityBus Enterprise Platform - Fare Evasion Detection & Ticket Audit Service
File: backend/services/fare_evasion_risk_scorer.py

Cross-references overhead infrared APC boarding pulses against AFC smart card taps
and mobile ticket scans to calculate station-level fare evasion leakages.
"""

from typing import Dict, List, Any, Optional


class FareEvasionRiskScorer:
    """Detects disparities between physical boardings and validated fares."""

    @staticmethod
    def audit_trip_fare_compliance(bus_id: int, total_apc_boardings: int, total_validated_tickets: int) -> Dict[str, Any]:
        """Calculates unpaid ride ratio and flags conductor inspection audits."""
        unaccounted_passengers = max(0, total_apc_boardings - total_validated_tickets)
        evasion_rate_pct = round((unaccounted_passengers / max(1, total_apc_boardings)) * 100.0, 1)

        risk_tier = "LOW"
        inspection_recommended = False

        if evasion_rate_pct >= 25.0:
            risk_tier = "CRITICAL_LEAKAGE"
            inspection_recommended = True
        elif evasion_rate_pct >= 12.0:
            risk_tier = "MODERATE_RISK"
            inspection_recommended = True

        return {
            "bus_id": bus_id,
            "total_physical_boardings": total_apc_boardings,
            "total_validated_fares": total_validated_tickets,
            "unaccounted_riders": unaccounted_passengers,
            "fare_evasion_rate_pct": evasion_rate_pct,
            "risk_tier": risk_tier,
            "dispatch_flying_squad_inspector": inspection_recommended,
            "estimated_revenue_leakage_inr": unaccounted_passengers * 22.0
        }
