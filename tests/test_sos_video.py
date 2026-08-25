"""
CityBus Enterprise Platform - SOS Video & Silent Duress Unit Tests
File: tests/test_sos_video.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.sos_video.live_camera_stream_relay import LiveCCTVStreamRelay
from services.sos_video.emergency_broadcast_mesh import EmergencyBroadcastMesh
from services.sos_video.silent_duress_alarm import SilentDuressAlarmEngine


class TestSOSVideoAndSilentDuress(unittest.TestCase):
    def test_live_cctv_stream_provisioning(self):
        streams = LiveCCTVStreamRelay.provision_emergency_streams(bus_id=1, bus_number="AP16-001")
        self.assertEqual(streams['active_camera_count'], 4)
        self.assertIn('stream_session_token', streams)
        self.assertEqual(len(streams['streams']), 4)

    def test_emergency_broadcast_mesh(self):
        broadcast = EmergencyBroadcastMesh.dispatch_emergency_broadcast(
            incident_id=202,
            bus_number="AP16-005",
            latitude=16.5062,
            longitude=80.6480
        )
        self.assertEqual(len(broadcast['dispatched_units']), 3)
        self.assertEqual(broadcast['status'], 'MULTI_AGENCY_INTERCEPT_DISPATCHED')

    def test_silent_duress_alarm(self):
        duress = SilentDuressAlarmEngine.trigger_silent_duress(
            bus_id=1,
            bus_number="AP16-001",
            driver_id=10,
            current_lat=16.5062,
            current_lng=80.6480
        )
        self.assertTrue(duress['in_cabin_indicators_suppressed'])
        self.assertEqual(duress['alarm_state'], 'SILENT_DURESS_ACTIVE')
        self.assertEqual(duress['police_112_priority'], 'PRIORITY_1_ARMED_INTERCEPT')


if __name__ == '__main__':
    unittest.main()
