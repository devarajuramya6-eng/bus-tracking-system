"""
CityBus Enterprise Platform - OppCharge & Pantograph Opportunity Charging Tests
File: tests/test_opportunity_charging.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.opportunity_charging.pantograph_docking_alignment import PantographDockingEngine
from services.opportunity_charging.superfast_dc_thermal_guard import SuperfastDCThermalGuard
from services.opportunity_charging.time_of_use_charge_arbitrage import TimeOfUseChargeOptimizer


class TestOpportunityCharging(unittest.TestCase):
    def test_pantograph_alignment_valid(self):
        res = PantographDockingEngine.verify_docking_alignment(
            bus_id=101,
            bus_number="AP16-E-101",
            lateral_offset_mm=45.0, # Within 150mm
            longitudinal_offset_mm=80.0,
            is_kneeling=True,
            is_handbrake_engaged=True
        )
        self.assertEqual(res['docking_status'], 'DOCKING_ALIGNED_READY')
        self.assertEqual(res['command'], 'LOWER_PANTOGRAPH_START_CHARGE')

    def test_pantograph_alignment_out_of_bounds(self):
        res = PantographDockingEngine.verify_docking_alignment(
            bus_id=101,
            bus_number="AP16-E-101",
            lateral_offset_mm=190.0, # Out of tolerance (> 150mm)
            longitudinal_offset_mm=80.0
        )
        self.assertEqual(res['docking_status'], 'ALIGNMENT_OUT_OF_BOUNDS')
        self.assertEqual(res['command'], 'REALIGN_VEHICLE')

    def test_dc_fast_charging_thermal_derating(self):
        guard = SuperfastDCThermalGuard.monitor_fast_charge(power_kw=450.0, contact_temp_c=70.0, coolant_flow_lpm=6.0) # > 68C
        self.assertTrue(guard['is_derated'])
        self.assertEqual(guard['delivered_power_kw'], 250.0)

    def test_tou_charge_arbitrage(self):
        off_peak = TimeOfUseChargeOptimizer.get_tariff_for_hour(2) # 02:00 AM
        self.assertEqual(off_peak['tariff_tier'], 'OFF_PEAK')
        self.assertTrue(off_peak['charging_authorized'])

        peak = TimeOfUseChargeOptimizer.get_tariff_for_hour(19) # 07:00 PM
        self.assertEqual(peak['tariff_tier'], 'PEAK')
        self.assertFalse(peak['charging_authorized'])


if __name__ == '__main__':
    unittest.main()
