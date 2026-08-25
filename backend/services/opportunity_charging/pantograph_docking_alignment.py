"""
CityBus Enterprise Platform - Inverted Pantograph Automated Docking Alignment
File: backend/services/opportunity_charging/pantograph_docking_alignment.py

Aligns electric buses beneath OppCharge (SAE J3105-1) top-down pantograph masts:
- Laser positioning checks lateral offset tolerance (+/- 150 mm)
- Longitudinal stopping bar verification (+/- 250 mm)
- Automatic pantograph drop authorization and DC contactor interlocking
"""

from typing import Dict, Any


class PantographDockingEngine:
    LATERAL_TOLERANCE_MM = 150.0
    LONGITUDINAL_TOLERANCE_MM = 250.0

    @staticmethod
    def verify_docking_alignment(bus_id: int, bus_number: str,
                                 lateral_offset_mm: float,
                                 longitudinal_offset_mm: float,
                                 is_kneeling: bool = True,
                                 is_handbrake_engaged: bool = True) -> Dict[str, Any]:
        """
        Verifies positioning safety before lowering high-voltage pantograph head.
        """
        is_lateral_aligned = abs(lateral_offset_mm) <= PantographDockingEngine.LATERAL_TOLERANCE_MM
        is_long_aligned = abs(longitudinal_offset_mm) <= PantographDockingEngine.LONGITUDINAL_TOLERANCE_MM

        is_safe_to_charge = is_lateral_aligned and is_long_aligned and is_handbrake_engaged

        action = 'LOWER_PANTOGRAPH_START_CHARGE' if is_safe_to_charge else 'REALIGN_VEHICLE'

        return {
            'bus_id': bus_id,
            'bus_number': bus_number,
            'lateral_offset_mm': round(lateral_offset_mm, 1),
            'longitudinal_offset_mm': round(longitudinal_offset_mm, 1),
            'is_within_lateral_window': is_lateral_aligned,
            'is_within_longitudinal_window': is_long_aligned,
            'is_handbrake_secured': is_handbrake_engaged,
            'docking_status': 'DOCKING_ALIGNED_READY' if is_safe_to_charge else 'ALIGNMENT_OUT_OF_BOUNDS',
            'command': action
        }
