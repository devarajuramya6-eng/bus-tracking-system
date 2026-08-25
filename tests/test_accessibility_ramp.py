"""
CityBus Enterprise Platform - Wheelchair Ramp & Accessibility Tests
File: tests/test_accessibility_ramp.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.accessibility_ramp.hydraulic_ramp_actuator import WheelchairRampActuator
from services.accessibility_ramp.wheelchair_bay_restraint_monitor import WheelchairBayRestraintMonitor
from services.accessibility_ramp.driver_accessibility_chime import AccessibilityDeploymentChime


class TestAccessibilityRamp(unittest.TestCase):
    def test_ramp_deployment_valid(self):
        dep = WheelchairRampActuator.deploy_ramp(
            curb_height_mm=170.0, # 270 - 170 = 100mm drop over 1000mm length = 10% slope
            ramp_length_mm=1000.0,
            is_obstruction_detected=False,
            vehicle_speed_kmh=0.0
        )
        self.assertTrue(dep['success'])
        self.assertEqual(dep['ramp_slope_gradient_pct'], 10.0)
        self.assertTrue(dep['is_accessible_slope_compliant'])

    def test_ramp_deployment_blocked_by_motion(self):
        dep = WheelchairRampActuator.deploy_ramp(
            curb_height_mm=170.0,
            is_obstruction_detected=False,
            vehicle_speed_kmh=15.0 # Moving
        )
        self.assertFalse(dep['success'])
        self.assertEqual(dep['ramp_state'], 'STOWED_LOCKED')

    def test_wheelchair_bay_restraints_secured(self):
        bay = WheelchairBayRestraintMonitor.audit_wheelchair_bay(
            is_bay_occupied=True,
            four_point_anchors_locked=True,
            lap_shoulder_belt_buckled=True
        )
        self.assertTrue(bay['is_safe_for_transit'])
        self.assertEqual(bay['departure_authorization'], 'AUTHORIZED')

    def test_accessibility_deployment_chime(self):
        sig = AccessibilityDeploymentChime.get_warning_signals(ramp_motion_state="DEPLOYING")
        self.assertTrue(sig['is_passenger_caution_active'])
        self.assertEqual(sig['exterior_audible_buzzer'], 'PULSATING_75DB_WARNING_CHIME')


if __name__ == '__main__':
    unittest.main()
