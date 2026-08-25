"""
CityBus Enterprise Platform - TPMS, Tire Health & Brake Wear Tests
File: tests/test_tire_health.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.tire_health.tpms_telemetry_parser import TPMSTelemetryParser
from services.tire_health.tire_rotation_scheduler import TireRotationScheduler
from services.tire_health.brake_lining_wear_sensor import BrakeLiningWearMonitor


class TestTireAndBrakeHealth(unittest.TestCase):
    def test_tpms_slow_puncture_detection(self):
        eval_tpms = TPMSTelemetryParser.evaluate_wheel_tpms(
            wheel_position="RLI",
            pressure_bar=6.8,
            temperature_c=54.0,
            pressure_drop_rate_bar_hr=0.45
        )
        self.assertTrue(eval_tpms['is_puncture_detected'])
        self.assertEqual(eval_tpms['status'], 'CRITICAL_PUNCTURE')

    def test_tire_rotation_due(self):
        res = TireRotationScheduler.audit_tire_set(
            bus_number="AP16-001",
            current_odometer_km=52000.0,
            last_rotation_km=24000.0, # 28,000 km since rotation (> 25k)
            min_tread_depth_mm=5.2
        )
        self.assertTrue(res['is_rotation_overdue'])
        self.assertEqual(res['maintenance_action'], 'SCHEDULE_TIRE_ROTATION')

    def test_brake_lining_wear_critical(self):
        brake = BrakeLiningWearMonitor.evaluate_brake_wear(axle_name="FRONT_STEER_AXLE", pad_thickness_mm=1.8)
        self.assertTrue(brake['is_critical_danger'])
        self.assertEqual(brake['maintenance_status'], 'CRITICAL_REPLACE_IMMEDIATELY')


if __name__ == '__main__':
    unittest.main()
