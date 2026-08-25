"""
CityBus Enterprise Platform - Ergonomic Whole-Body Vibration (WBV) Monitor
File: backend/services/driver_wellness/ergonomic_vibration_index.py

Calculates daily Whole-Body Vibration (WBV) per ISO 2631-1 standard:
- Daily Vibration Dose Value: VDV = (Integral(a_w^4 * dt))^(1/4) m/s^1.75
- Exposure Action Value (EAV = 9.1 m/s^1.75) triggers seat suspension damper adjustment
- Exposure Limit Value (ELV = 21.0 m/s^1.75) requires duty relief
"""

from typing import Dict, Any, List


class ErgonomicVibrationMonitor:
    EAV_THRESHOLD = 9.1
    ELV_THRESHOLD = 21.0

    @staticmethod
    def calculate_vdv(weighted_accel_z_samples: List[float], dt_seconds: float = 0.5) -> Dict[str, Any]:
        """
        Calculates cumulative Vibration Dose Value (VDV) from seat accelerometer.
        """
        if not weighted_accel_z_samples:
            return {'vdv_score': 0.0, 'status': 'NO_DATA'}

        # Integral of a_w^4
        integral_a4 = sum((abs(a) ** 4) * dt_seconds for a in weighted_accel_z_samples)
        vdv = integral_a4 ** 0.25

        is_elv_exceeded = vdv >= ErgonomicVibrationMonitor.ELV_THRESHOLD
        is_eav_exceeded = vdv >= ErgonomicVibrationMonitor.EAV_THRESHOLD

        status = 'CRITICAL_ERGONOMIC_RELIEF_REQUIRED' if is_elv_exceeded else ('WARNING_ACTION_REQUIRED' if is_eav_exceeded else 'HEALTHY_ERGONOMICS')

        return {
            'vdv_score': round(vdv, 2),
            'iso_standard': 'ISO_2631_1_WHOLE_BODY_VIBRATION',
            'action_threshold_eav': ErgonomicVibrationMonitor.EAV_THRESHOLD,
            'limit_threshold_elv': ErgonomicVibrationMonitor.ELV_THRESHOLD,
            'is_action_value_exceeded': is_eav_exceeded,
            'is_limit_value_exceeded': is_elv_exceeded,
            'health_status': status,
            'recommended_remedy': 'Inspect pneumatic seat air suspension damper.' if is_eav_exceeded else 'Driver posture and seat damping normal.'
        }
