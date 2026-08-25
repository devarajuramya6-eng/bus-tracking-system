"""
CityBus Enterprise Platform - Platform Edge Safety & Sonar Tests
File: tests/test_platform_safety.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.platform_safety.edge_door_interlock_guard import EdgeDoorInterlockGuard
from services.platform_safety.surge_crowd_platform_announcer import SurgeCrowdAnnouncer
from services.platform_safety.blind_spot_pedestrian_sonar import BlindSpotPedestrianRadar


class TestPlatformSafety(unittest.TestCase):
    def test_traction_interlock_secured(self):
        lock = EdgeDoorInterlockGuard.verify_traction_interlock(
            door_front_closed=True,
            door_rear_closed=True,
            is_anti_pinch_triggered=False,
            is_ramp_stowed=True
        )
        self.assertFalse(lock['traction_motor_inhibited'])
        self.assertEqual(lock['traction_authorization'], 'ACCELERATION_AUTHORIZED')

    def test_traction_interlock_door_ajar(self):
        lock = EdgeDoorInterlockGuard.verify_traction_interlock(
            door_front_closed=False,
            door_rear_closed=True,
            is_anti_pinch_triggered=False,
            is_ramp_stowed=True
        )
        self.assertTrue(lock['traction_motor_inhibited'])
        self.assertEqual(lock['traction_authorization'], 'TRACTION_INTERLOCK_ACTIVE_HOLD')

    def test_surge_crowd_platform_announcement(self):
        ann = SurgeCrowdAnnouncer.evaluate_platform_announcement(
            approaching_bus_number="AP16-004",
            approaching_bus_occ_pct=95.0, # Crush load
            trailing_bus_number="AP16-008",
            trailing_bus_eta_min=3.0,
            trailing_bus_occ_pct=40.0
        )
        self.assertTrue(ann['is_crowd_bypass_active'])
        self.assertIn('AP16-004', ann['announcement_english'])
        self.assertIn('AP16-008', ann['announcement_telugu'])

    def test_blind_spot_pedestrian_sonar_warning(self):
        sensors = [
            {'zone': 'LEFT_KERB', 'distance_m': 1.0, 'detected_object': 'PEDESTRIAN'},
            {'zone': 'FRONT', 'distance_m': 4.0, 'detected_object': 'CAR'}
        ]
        radar = BlindSpotPedestrianRadar.evaluate_blind_spots(sensors)
        self.assertEqual(radar['detected_hazards_count'], 1)
        self.assertTrue(radar['is_emergency_audio_alarm_active'])
        self.assertEqual(radar['cockpit_hmi_state'], 'RED_ALERT_BRAKE_IMMEDIATELY')


if __name__ == '__main__':
    unittest.main()
