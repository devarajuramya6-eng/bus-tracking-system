"""
CityBus Enterprise Platform - Regenerative Braking & Supercapacitor Tests
File: tests/test_regenerative_braking.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.regenerative_braking.regen_torque_blending import RegenTorqueBlendingEngine
from services.regenerative_braking.supercapacitor_buffer_state import SupercapacitorBufferState
from services.regenerative_braking.regen_energy_audit import RegenEnergyAuditor


class TestRegenerativeBraking(unittest.TestCase):
    def test_regen_torque_blending_low_pedal(self):
        blend = RegenTorqueBlendingEngine.blend_brake_torque(
            pedal_displacement_pct=25.0, # Light braking
            vehicle_speed_kmh=40.0,
            battery_soc_pct=75.0
        )
        self.assertEqual(blend['friction_pneumatic_torque_nm'], 0.0)
        self.assertTrue(blend['is_brake_pad_wear_prevented'])
        self.assertGreater(blend['regenerative_torque_nm'], 1000.0)

    def test_regen_torque_derating_full_battery(self):
        blend = RegenTorqueBlendingEngine.blend_brake_torque(
            pedal_displacement_pct=50.0,
            vehicle_speed_kmh=40.0,
            battery_soc_pct=99.0 # Full battery (>98%)
        )
        self.assertEqual(blend['regenerative_torque_nm'], 0.0)
        self.assertGreater(blend['friction_pneumatic_torque_nm'], 0.0)

    def test_supercapacitor_stored_energy(self):
        cap = SupercapacitorBufferState.calculate_stored_energy(voltage_v=44.0)
        self.assertGreater(cap['stored_energy_wh'], 10.0)
        self.assertEqual(cap['buffer_mode'], 'READY_FOR_BOOST_DISCHARGE')

    def test_shift_regen_energy_audit(self):
        audit = RegenEnergyAuditor.audit_shift_regen(
            bus_number="AP16-E-101",
            total_distance_km=220.0,
            total_energy_consumed_kwh=190.0,
            total_energy_regen_kwh=42.0
        )
        self.assertGreater(audit['energy_recovery_ratio_pct'], 20.0)
        self.assertGreater(audit['shift_electricity_savings_inr'], 200.0)


if __name__ == '__main__':
    unittest.main()
