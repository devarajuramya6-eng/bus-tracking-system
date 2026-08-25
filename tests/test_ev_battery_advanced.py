"""
CityBus Enterprise Platform - Advanced EV Battery & Cell Balancer Tests
File: tests/test_ev_battery_advanced.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.ev_battery.cell_voltage_equalizer import BatteryCellEqualizer
from services.ev_battery.internal_resistance_estimator import BatteryInternalResistanceEstimator
from services.ev_battery.depth_of_discharge_optimizer import DepthOfDischargeOptimizer


class TestEVBatteryAdvanced(unittest.TestCase):
    def test_cell_voltage_balancing_trigger(self):
        voltages = [3.280] * 15 + [3.305] # 25mV delta
        res = BatteryCellEqualizer.analyze_pack_cells("PACK-01", voltages)
        self.assertTrue(res['is_balancing_active'])
        self.assertAlmostEqual(res['delta_v_millivolts'], 25.0, places=1)

    def test_dcir_internal_resistance_estimation(self):
        res = BatteryInternalResistanceEstimator.estimate_dcir(
            voltage_before_pulse_v=680.0,
            voltage_during_pulse_v=672.0, # 8V drop
            current_pulse_amperes=400.0   # 400A -> 8/400 = 0.020 ohm = 20 mohm
        )
        self.assertEqual(res['measured_dcir_mohm'], 20.0)
        self.assertEqual(res['battery_module_health'], 'HEALTHY_NOMINAL')

    def test_depth_of_discharge_optimizer(self):
        opt = DepthOfDischargeOptimizer.calculate_optimal_charge_limit(route_km=120.0)
        self.assertGreater(opt['recommended_charge_ceiling_soc_pct'], 60.0)
        self.assertGreater(opt['expected_battery_cycle_life'], 3000)


if __name__ == '__main__':
    unittest.main()
