"""
CityBus Enterprise Platform - Safety, ADAS & EV Thermal Unit Tests
File: tests/test_safety.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.safety.driver_fatigue_monitor import DriverFatigueMonitor
from services.safety.speed_governor_enforcement import SpeedGovernorEnforcement
from services.safety.ev_fire_thermal_runaway import EVThermalRunawayMonitor


class TestSafetyAndADAS(unittest.TestCase):
    def test_driver_fatigue_critical_alert(self):
        alert = DriverFatigueMonitor.evaluate_fatigue_telemetry(
            bus_id=1,
            driver_id=10,
            speed_kmh=45.0,
            perclos_ratio=0.38, # > 35% critical
            micro_sleep_duration_sec=2.0, # > 1.5s
            yawns_last_5min=6
        )
        self.assertEqual(alert['alert_level'], 'CRITICAL_FATIGUE_EMERGENCY')
        self.assertTrue(alert['cockpit_buzzer'])
        self.assertTrue(alert['dispatch_alert'])

    def test_speed_governor_tamper_audit(self):
        audit = SpeedGovernorEnforcement.audit_speed_governor(
            bus_id=5,
            bus_number="AP16-005",
            current_speed_kmh=68.0,
            governor_pulse_active=False, # Tampered wire
            throttle_pct=85.0
        )
        self.assertEqual(audit['alert_type'], 'SPEED_GOVERNOR_TAMPER_DETECTED')
        self.assertEqual(audit['severity'], 'CRITICAL')

    def test_ev_battery_thermal_runaway(self):
        ev_eval = EVThermalRunawayMonitor.evaluate_pack_telemetry(
            bus_id=101,
            max_cell_temp_c=65.0, # > 62C critical
            min_cell_temp_c=52.0,
            gas_sensor_ppm=58.0,
            insulation_resistance_kohm=80.0
        )
        self.assertEqual(ev_eval['status'], 'CRITICAL_THERMAL_RUNAWAY_TRIGGERED')
        self.assertTrue(ev_eval['doors_emergency_unlock'])


if __name__ == '__main__':
    unittest.main()
