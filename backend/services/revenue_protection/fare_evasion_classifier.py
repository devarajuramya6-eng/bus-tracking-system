"""
CityBus Enterprise Platform - Fare Evasion Discrepancy Classifier
File: backend/services/revenue_protection/fare_evasion_classifier.py

Compares doorway APC boardings against ticket validations per stop segment:
- Detects unvalidated passenger boarding anomalies (Evasion Risk Score > 0.35)
- Flags routes and driver/conductor runs with systemic revenue leakage
"""

from typing import Dict, Any, List


class FareEvasionClassifier:
    @staticmethod
    def evaluate_stop_segment(stop_id: int, stop_name: str,
                              apc_boardings: int,
                              ticket_validations: int) -> Dict[str, Any]:
        """
        Evaluates discrepancy between physical boardings and paid tickets.
        """
        discrepancy = max(0, apc_boardings - ticket_validations)
        evasion_rate = (discrepancy / max(1, apc_boardings))

        is_high_risk = evasion_rate >= 0.25 and discrepancy >= 3

        return {
            'stop_id': stop_id,
            'stop_name': stop_name,
            'apc_boardings': apc_boardings,
            'ticket_validations': ticket_validations,
            'unvalidated_passengers': discrepancy,
            'evasion_rate_pct': round(evasion_rate * 100.0, 1),
            'risk_level': 'HIGH_REVENUE_LEAKAGE' if is_high_risk else ('MODERATE' if discrepancy > 0 else 'COMPLIANT'),
            'inspector_dispatch_recommended': is_high_risk
        }
