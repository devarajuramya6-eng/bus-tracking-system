"""
CityBus Enterprise Platform - Driver Mobile Phone & Visual Distraction Classifier
File: backend/services/driver_vision_ai/mobile_phone_distraction_classifier.py

Classifies driver cognitive and manual distraction from cockpit edge AI stream:
- PHONE_CALL_HAND_HELD: Mobile device held against ear while moving (> 10 km/h)
- TEXTING_DOWNWARD_GAZE: Head pitch angle > 25° downwards for > 2.0 seconds
- SMOKING_OR_EATING: Hand-to-mouth repetitive objects
"""

from typing import Dict, Any


class DriverDistractionClassifier:
    @staticmethod
    def classify_driver_behavior(detected_object: str,
                                 head_pitch_deg: float,
                                 gaze_off_road_sec: float,
                                 vehicle_speed_kmh: float) -> Dict[str, Any]:
        """
        Evaluates visual distraction severity.
        """
        is_phone = detected_object.upper() in ('CELL_PHONE', 'MOBILE_DEVICE')
        is_prolonged_off_road_gaze = gaze_off_road_sec >= 2.0
        is_moving = vehicle_speed_kmh >= 5.0

        if is_phone and is_moving:
            severity = 'CRITICAL_ILLEGAL_PHONE_USE'
            cmd = 'TRIGGER_COCKPIT_VOICE_WARNING_AND_OCC_SNAPSHOT'
        elif is_prolonged_off_road_gaze and is_moving:
            severity = 'FORWARD_ROAD_ATTENTION_LOST'
            cmd = 'TRIGGER_ATTENTION_CHIME'
        else:
            severity = 'ATTENTIVE'
            cmd = 'STANDBY'

        return {
            'detected_object': detected_object,
            'gaze_off_road_duration_sec': round(gaze_off_road_sec, 1),
            'vehicle_speed_kmh': round(vehicle_speed_kmh, 1),
            'distraction_severity': severity,
            'corrective_action': cmd,
            'is_violation_recorded': severity != 'ATTENTIVE'
        }
