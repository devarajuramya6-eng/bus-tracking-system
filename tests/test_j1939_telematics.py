"""
CityBus Enterprise Platform - SAE J1939 CAN-Bus Telematics Tests
File: tests/test_j1939_telematics.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.j1939_telematics.pgn_spn_multiplexer import J1939PGNSPNDecoder
from services.j1939_telematics.transmission_retarder_monitor import RetarderTelemetryMonitor
from services.j1939_telematics.turbocharger_boost_diagnostics import TurbochargerBoostDiagnostics


class TestJ1939Telematics(unittest.TestCase):
    def test_j1939_eec1_rpm_decode(self):
        # 1600 RPM = 1600 / 0.125 = 12800 = 0x3200 (little endian: 0x00, 0x32)
        payload = bytes([0x7D, 0xC8, 0xFA, 0x00, 0x32, 0xFF, 0xFF, 0xFF])
        decoded = J1939PGNSPNDecoder.decode_eec1_frame(0x0CF00400, payload)
        self.assertEqual(decoded['pgn'], 61444)
        self.assertEqual(decoded['engine_speed_rpm'], 1600.0)

    def test_retarder_overheat_alert(self):
        res = RetarderTelemetryMonitor.process_retarder_telemetry(retarder_torque_pct=45.0, oil_temp_c=152.0) # > 145C
        self.assertTrue(res['is_thermal_overload'])
        self.assertEqual(res['status'], 'CRITICAL_RETARDER_OVERHEAT')

    def test_turbocharger_boost_leak_detection(self):
        diag = TurbochargerBoostDiagnostics.audit_boost_performance(
            engine_load_pct=90.0,
            boost_pressure_bar=0.85, # Low boost under high load
            egt_c=520.0
        )
        self.assertTrue(diag['is_boost_leak_suspected'])
        self.assertEqual(diag['diagnostics_state'], 'BOOST_LEAK_DETECTED')


if __name__ == '__main__':
    unittest.main()
