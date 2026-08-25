"""
CityBus Enterprise Platform - V2X & Transit Signal Priority Tests
File: tests/test_v2x_tsp.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.v2x_tsp.ntcip_1211_priority_request import NTCIP1211PriorityEngine
from services.v2x_tsp.green_light_optimal_speed_advisory import GLOSASpeedAdvisory
from services.v2x_tsp.dsrc_bsm_encoder import DSRCBasicSafetyMessageEncoder


class TestV2XAndTSP(unittest.TestCase):
    def test_ntcip_1211_priority_request_high_delay(self):
        spr = NTCIP1211PriorityEngine.generate_spr_message(
            bus_id=1,
            bus_number="AP16-001",
            intersection_id="INT-BENZ-01",
            eta_to_stop_line_sec=15.0,
            delay_minutes=6.0, # High delay
            passenger_count=45
        )
        self.assertEqual(spr['assigned_priority_level'], 7)
        self.assertTrue(spr['priority_request_active'])
        self.assertEqual(spr['controller_command'], 'EXTEND_GREEN_PHASE_12S')

    def test_glosa_speed_advisory_green(self):
        adv = GLOSASpeedAdvisory.calculate_optimal_speed(
            distance_to_signal_m=300.0,
            signal_current_phase='GREEN',
            time_to_next_phase_sec=30.0,
            current_speed_kmh=35.0
        )
        self.assertEqual(adv['driver_advisory_action'], 'MAINTAIN_CRUISE_FOR_GREEN')
        self.assertTrue(adv['green_wave_catchable'])

    def test_dsrc_bsm_encoding(self):
        bsm = DSRCBasicSafetyMessageEncoder.encode_bsm_frame(
            bus_id=1,
            bus_number="AP16-001",
            lat=16.5062,
            lng=80.6480,
            speed_kmh=40.0,
            heading_deg=90.0,
            is_braking=False,
            passenger_count=35
        )
        self.assertEqual(bsm['standard'], 'SAE_J2735_2020')
        self.assertEqual(bsm['temporary_vehicle_id'], 'BUS-0001')


if __name__ == '__main__':
    unittest.main()
