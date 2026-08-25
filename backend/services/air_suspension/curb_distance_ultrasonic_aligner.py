"""
CityBus Enterprise Platform - Ultrasonic Platform Curb Distance Aligner
File: backend/services/air_suspension/curb_distance_ultrasonic_aligner.py

Measures lateral distance between bus entrance step and platform curb edge (Kassel kerb):
- Target gap: < 50 mm (Allows roll-on wheelchair / stroller access without manual ramp)
- Alarms if tire scrub / rim impact risk (< 20 mm) or excessive step gap (> 100 mm)
"""

from typing import Dict, Any


class CurbUltrasonicAligner:
    TARGET_GAP_MM = 50.0
    MAX_ALLOWABLE_GAP_MM = 100.0
    MIN_RIM_CLEARANCE_MM = 20.0

    @staticmethod
    def evaluate_docking_gap(lateral_curb_distance_mm: float) -> Dict[str, Any]:
        """
        Evaluates boarding gap safety.
        """
        is_rim_danger = lateral_curb_distance_mm < CurbUltrasonicAligner.MIN_RIM_CLEARANCE_MM
        is_step_gap_excessive = lateral_curb_distance_mm > CurbUltrasonicAligner.MAX_ALLOWABLE_GAP_MM
        is_perfect_dock = (not is_rim_danger) and (not is_step_gap_excessive)

        if is_rim_danger:
            status = 'TIRE_SCRUB_WARNING_STEER_LEFT'
        elif is_step_gap_excessive:
            status = 'EXCESSIVE_GAP_DEPLOY_RAMP'
        else:
            status = 'PERFECT_KASSEL_DOCK_STEP_FREE'

        return {
            'lateral_curb_distance_mm': round(lateral_curb_distance_mm, 1),
            'target_dock_distance_mm': CurbUltrasonicAligner.TARGET_GAP_MM,
            'is_step_free_accessible': is_perfect_dock,
            'is_manual_ramp_required': is_step_gap_excessive,
            'docking_alignment_status': status
        }
