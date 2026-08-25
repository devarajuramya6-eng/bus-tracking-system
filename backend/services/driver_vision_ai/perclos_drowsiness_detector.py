"""
CityBus Enterprise Platform - PERCLOS Eye Closure Driver Drowsiness Detector
File: backend/services/driver_vision_ai/perclos_drowsiness_detector.py

Evaluates near-infrared cabin camera eye-gaze telemetry using PERCLOS (P80 standard):
- PERCLOS: Percentage of time eyes are >= 80% closed over 60-second sliding window
- Drowsiness Threshold: PERCLOS > 12.0% triggers Level 1 Driver Alert
- Microsleep Threshold: Eye closure duration > 1.5 seconds triggers Emergency Alert & Dispatch Intercept
"""

from typing import Dict, Any


class PERCLOSDrowsinessDetector:
    PERCLOS_WARNING_THRESHOLD_PCT = 12.0
    MICROSLEEP_SECONDS_THRESHOLD = 1.5

    @staticmethod
    def evaluate_drowsiness(perclos_score_pct: float,
                            max_single_blink_duration_sec: float,
                            yawn_count_last_5min: int) -> Dict[str, Any]:
        """
        Evaluates driver alertness and fatigue risk.
        """
        is_microsleep = max_single_blink_duration_sec >= PERCLOSDrowsinessDetector.MICROSLEEP_SECONDS_THRESHOLD
        is_fatigued = perclos_score_pct >= PERCLOSDrowsinessDetector.PERCLOS_WARNING_THRESHOLD_PCT or yawn_count_last_5min >= 4

        if is_microsleep:
            alert_level = 'CRITICAL_MICROSLEEP_DETECTED'
            action = 'TRIGGER_IMMEDIATE_CABIN_HAPTIC_AND_SIREN'
        elif is_fatigued:
            alert_level = 'MODERATE_FATIGUE_WARNING'
            action = 'AUDIO_VOICE_ALERT_AND_DISPATCH_LOG'
        else:
            alert_level = 'ALERT_AND_ATTENTIVE'
            action = 'NO_ACTION'

        return {
            'perclos_percentage': round(perclos_score_pct, 1),
            'max_blink_duration_seconds': round(max_single_blink_duration_sec, 2),
            'yawn_count': yawn_count_last_5min,
            'alertness_state': alert_level,
            'system_response': action,
            'is_driver_safe': not (is_microsleep or is_fatigued)
        }
