"""
CityBus Enterprise Platform - Telematics & CAN-Bus Unit Tests
File: tests/test_telematics.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.telematics.canbus_decoder import CANBusDecoder
from services.telematics.dtc_analyzer import DTCAnalyzer
from services.telematics.driver_scoring import DriverBehaviorScorer
from services.telematics.fuel_flow_sensor import FuelFlowSensorEngine


class TestTelematics(unittest.TestCase):
    def test_canbus_obd2_decoder(self):
        # RPM test (PID 0x0C)
        res = CANBusDecoder.decode_obd2_frame("0C", "1A F8") # ((26*256)+248)/4 = 1726 RPM
        self.assertEqual(res['parameter'], 'ENGINE_RPM')
        self.assertAlmostEqual(res['value'], 1726.0, places=1)

        # Coolant Temp test (PID 0x05)
        res_temp = CANBusDecoder.decode_obd2_frame("05", "78") # 120 - 40 = 80 deg C
        self.assertEqual(res_temp['parameter'], 'ENGINE_COOLANT_TEMP')
        self.assertEqual(res_temp['value'], 80)

    def test_dtc_analyzer(self):
        res = DTCAnalyzer.analyze_fault_code("P0217", bus_id=10)
        self.assertEqual(res['severity'], 'Critical')
        self.assertTrue(res['requires_immediate_halt'])

    def test_driver_behavior_scoring(self):
        telemetry = [
            {'speed': 40.0, 'engine_rpm': 1400},
            {'speed': 25.0, 'engine_rpm': 1100}, # -15 km/h -> Harsh brake
            {'speed': 28.0, 'engine_rpm': 1200}
        ]
        score = DriverBehaviorScorer.calculate_shift_score(telemetry)
        self.assertIn('safety_score', score)
        self.assertGreaterEqual(score['safety_score'], 50.0)

    def test_fuel_theft_detection(self):
        fuel_series = [
            {'bus_id': 10, 'liters': 180.0, 'speed': 0.0, 'timestamp': '10:00'},
            {'bus_id': 10, 'liters': 145.0, 'speed': 0.0, 'timestamp': '10:05', 'lat': 16.51, 'lng': 80.61} # 35L drop stationary
        ]
        anomalies = FuelFlowSensorEngine.detect_theft_anomaly(fuel_series, drop_threshold_liters=15.0)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'FUEL_THEFT_DETECTED')


if __name__ == '__main__':
    unittest.main()
