"""
CityBus Enterprise Platform - Electric Vehicle (EV) Unit Tests
File: tests/test_ev.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.ev.battery_degradation_model import BatteryDegradationModel
from services.ev.smart_charging_scheduler import SmartChargingScheduler
from services.ev.regenerative_braking_analyzer import RegenerativeBrakingAnalyzer


class TestEVSystems(unittest.TestCase):
    def test_battery_degradation_soh(self):
        soh_data = BatteryDegradationModel.estimate_soh(equivalent_full_cycles=500, avg_ambient_temp_c=32.0)
        self.assertIn('soh_percentage', soh_data)
        self.assertGreater(soh_data['soh_percentage'], 75.0)
        self.assertEqual(soh_data['battery_status'], 'EXCELLENT')

    def test_smart_charging_scheduler(self):
        fleet = [
            {'bus_id': 1, 'bus_number': 'AP16-E-01', 'soc_percentage': 30.0},
            {'bus_id': 2, 'bus_number': 'AP16-E-02', 'soc_percentage': 55.0},
            {'bus_id': 3, 'bus_number': 'AP16-E-03', 'soc_percentage': 92.0} # Doesn't need charge
        ]
        schedule = SmartChargingScheduler.generate_charging_schedule(fleet)
        self.assertEqual(len(schedule['active_charging']), 2)
        self.assertGreater(schedule['total_power_allocated_kw'], 0.0)

    def test_regenerative_braking_energy(self):
        energy = RegenerativeBrakingAnalyzer.analyze_trip_energy(distance_km=15.0, stops_count=12)
        self.assertGreater(energy['regen_recovered_kwh'], 0.0)
        self.assertGreater(energy['efficiency_kwh_per_km'], 0.5)


if __name__ == '__main__':
    unittest.main()
