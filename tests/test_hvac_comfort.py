"""
CityBus Enterprise Platform - HVAC, Thermal Comfort & Air Quality Tests
File: tests/test_hvac_comfort.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.hvac_comfort.thermal_comfort_pmv import ThermalComfortModel
from services.hvac_comfort.ev_ac_range_optimizer import EVHVACRangeOptimizer
from services.hvac_comfort.co2_air_quality_ventilator import CabinAirQualityVentilator


class TestHVACAndThermalComfort(unittest.TestCase):
    def test_pmv_thermal_comfort_calculation(self):
        res = ThermalComfortModel.calculate_pmv_ppd(cabin_temp_c=24.0, relative_humidity_pct=50.0, passenger_count=25)
        self.assertTrue(res['is_within_ashrae55_standard'])
        self.assertLess(res['ppd_dissatisfied_pct'], 20.0)

    def test_ev_hvac_power_throttling_low_battery(self):
        res = EVHVACRangeOptimizer.optimize_hvac_draw(
            battery_soc_pct=15.0, # Low battery (< 18%)
            ambient_temp_c=42.0,
            remaining_route_distance_km=15.0,
            estimated_driving_range_km=18.0
        )
        self.assertEqual(res['hvac_operating_mode'], 'EMERGENCY_ECO_THROTTLE')
        self.assertLessEqual(res['max_allowable_hvac_kw'], 5.0)

    def test_co2_air_quality_stale_air_purge(self):
        vent = CabinAirQualityVentilator.evaluate_cabin_air_quality(co2_ppm=1400.0) # > 1200 ppm
        self.assertEqual(vent['fresh_air_damper_position_pct'], 100)
        self.assertEqual(vent['ventilation_mode'], 'STALE_AIR_PURGE_TRIGGERED')


if __name__ == '__main__':
    unittest.main()
