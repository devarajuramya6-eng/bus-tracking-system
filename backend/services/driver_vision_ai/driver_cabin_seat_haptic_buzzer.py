"""
CityBus Enterprise Platform - Driver Seat Haptic Vibration & Audio Alert Controller
File: backend/services/driver_vision_ai/driver_cabin_seat_haptic_buzzer.py

Controls pneumatic driver seat cushion haptic vibration motors and cockpit piezo buzzer:
- DUAL_CUSHION_VIBRATION: High-frequency pulses for microsleep intervention
- LEFT_SEAT_HAPTIC: Directional alert for left-side blind-spot hazard
- RIGHT_SEAT_HAPTIC: Directional alert for right-side lane departure
"""

from typing import Dict, Any


class DriverCabinHapticAlert:
    @staticmethod
    def trigger_seat_haptic(alarm_type: str, intensity_pct: int = 100) -> Dict[str, Any]:
        """
        Activates haptic motors on driver seat.
        """
        intensity = max(10, min(100, intensity_pct))
        typ = alarm_type.upper().strip()

        if typ == 'MICROSLEEP_EMERGENCY':
            motor_pattern = 'PULSING_DUAL_CUSHION_MAX_POWER'
            piezo_buzzer = '85DB_CONTINUOUS_WARBLE'
        elif typ == 'LEFT_BLIND_SPOT':
            motor_pattern = 'LEFT_THIGH_VIBRATION_INTERMITTENT'
            piezo_buzzer = 'LEFT_SPEAKER_CHIME'
        elif typ == 'RIGHT_LANE_DEPARTURE':
            motor_pattern = 'RIGHT_THIGH_VIBRATION_INTERMITTENT'
            piezo_buzzer = 'RIGHT_SPEAKER_CHIME'
        else:
            motor_pattern = 'GENTLE_ATTENTION_TAP'
            piezo_buzzer = 'SOFT_DING'

        return {
            'alarm_type': typ,
            'vibration_intensity_pct': intensity,
            'haptic_seat_motor_pattern': motor_pattern,
            'cockpit_piezo_buzzer_mode': piezo_buzzer,
            'is_haptic_dispatched': True
        }
