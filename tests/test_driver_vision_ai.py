"""
CityBus Enterprise Platform - Driver Vision AI & Attention Tests
File: tests/test_driver_vision_ai.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.driver_vision_ai.perclos_drowsiness_detector import PERCLOSDrowsinessDetector
from services.driver_vision_ai.mobile_phone_distraction_classifier import DriverDistractionClassifier
from services.driver_vision_ai.driver_cabin_seat_haptic_buzzer import DriverCabinHapticAlert


class TestDriverVisionAI(unittest.TestCase):
    def test_perclos_drowsiness_nominal(self):
        eval_alert = PERCLOSDrowsinessDetector.evaluate_drowsiness(
            perclos_score_pct=4.5,
            max_single_blink_duration_sec=0.3,
            yawn_count_last_5min=0
        )
        self.assertTrue(eval_alert['is_driver_safe'])
        self.assertEqual(eval_alert['alertness_state'], 'ALERT_AND_ATTENTIVE')

    def test_perclos_microsleep_emergency(self):
        eval_micro = PERCLOSDrowsinessDetector.evaluate_drowsiness(
            perclos_score_pct=18.0,
            max_single_blink_duration_sec=1.8, # > 1.5s
            yawn_count_last_5min=3
        )
        self.assertFalse(eval_micro['is_driver_safe'])
        self.assertEqual(eval_micro['alertness_state'], 'CRITICAL_MICROSLEEP_DETECTED')

    def test_driver_phone_distraction_moving(self):
        cls = DriverDistractionClassifier.classify_driver_behavior(
            detected_object="CELL_PHONE",
            head_pitch_deg=10.0,
            gaze_off_road_sec=2.5,
            vehicle_speed_kmh=35.0
        )
        self.assertTrue(cls['is_violation_recorded'])
        self.assertEqual(cls['distraction_severity'], 'CRITICAL_ILLEGAL_PHONE_USE')

    def test_driver_seat_haptic_alarm(self):
        hap = DriverCabinHapticAlert.trigger_seat_haptic(alarm_type="MICROSLEEP_EMERGENCY", intensity_pct=100)
        self.assertTrue(hap['is_haptic_dispatched'])
        self.assertEqual(hap['haptic_seat_motor_pattern'], 'PULSING_DUAL_CUSHION_MAX_POWER')


if __name__ == '__main__':
    unittest.main()
