"""
CityBus Enterprise Platform - Electric Bus Thermal Management & Heat Pump Tests
File: tests/test_thermal_inverter.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.thermal_inverter.refrigerant_flow_controller import HeatPumpRefrigerantController
from services.thermal_inverter.battery_glycol_chiller_loop import BatteryGlycolChillerLoop
from services.thermal_inverter.compressor_vfd_power_modulator import CompressorVFDModulator


class TestThermalInverter(unittest.TestCase):
    def test_heat_pump_waste_heat_harvesting(self):
        hp = HeatPumpRefrigerantController.select_heat_pump_mode(
            ambient_temp_c=12.0,
            target_cabin_temp_c=22.0,
            motor_coolant_temp_c=50.0 # Hot motor
        )
        self.assertEqual(hp['operating_mode'], 'MOTOR_WASTE_HEAT_HARVESTING')
        self.assertTrue(hp['is_waste_heat_utilized'])
        self.assertGreater(hp['estimated_cop'], 3.0)

    def test_battery_glycol_chiller_cooling_active(self):
        loop = BatteryGlycolChillerLoop.regulate_battery_thermal_loop(
            avg_battery_cell_temp_c=35.0, # > 33.0C
            ambient_temp_c=40.0
        )
        self.assertTrue(loop['is_refrigerant_chiller_active'])
        self.assertEqual(loop['thermal_regulation_mode'], 'ACTIVE_REFRIGERANT_CHILLER_COOLING')
        self.assertEqual(loop['glycol_pump_flow_lpm'], 42.0)

    def test_compressor_vfd_power_modulation(self):
        mod = CompressorVFDModulator.calculate_compressor_power(
            cabin_temp_error_c=4.5,
            passenger_count=35
        )
        self.assertGreater(mod['target_compressor_rpm'], 2000)
        self.assertGreater(mod['electrical_power_draw_kw'], 2.0)
        self.assertEqual(mod['compressor_inverter_status'], 'MODULATED_SPEED_RUNNING')


if __name__ == '__main__':
    unittest.main()
