"""
CityBus Enterprise Platform - Tire Casing Laser Shearography NDT Analyzer
File: backend/services/retread_ndt/casing_shearography_analyzer.py

Analyzes vacuum laser shearography interferograms on 295/80R22.5 tire casings:
- Detects subsurface belt edge separation anomalies (Phase fringe distortions)
- Detects radial ply air pockets and carcass bead blisters
- Authorizes or rejects casing for Precured Cold Retreading (Procure)
"""

from typing import List, Dict, Any


class TireShearographyAnalyzer:
    MAX_ALLOWABLE_FRINGE_ANOMALIES = 0 # Zero tolerance for structural belt separation

    @staticmethod
    def evaluate_casing_scan(tire_serial_number: str, retread_count: int,
                             anomaly_count: int, max_fringe_diameter_mm: float) -> Dict[str, Any]:
        """
        Evaluates shearography scan result for casing integrity.
        """
        # Max 3 retreads allowed per commercial municipal casing
        is_retread_limit_reached = retread_count >= 3
        has_critical_defect = anomaly_count > 0 or max_fringe_diameter_mm > 5.0

        is_approved = (not is_retread_limit_reached) and (not has_critical_defect)

        if not is_approved:
            if is_retread_limit_reached:
                decision = 'REJECT_CASING_MAX_RETREAD_LIFE_REACHED'
            else:
                decision = 'REJECT_CASING_INTERNAL_PLY_SEPARATION'
        else:
            decision = 'APPROVE_FOR_PRECURED_RETREADING'

        return {
            'tire_serial_number': tire_serial_number,
            'current_retread_count': retread_count,
            'laser_anomalies_detected': anomaly_count,
            'max_anomaly_diameter_mm': round(max_fringe_diameter_mm, 1),
            'is_casing_sound': not has_critical_defect,
            'casing_decision': decision,
            'procure_approval': is_approved
        }
