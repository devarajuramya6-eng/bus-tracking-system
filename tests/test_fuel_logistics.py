"""
CityBus Enterprise Platform - Fuel Logistics & ATG Tests
File: tests/test_fuel_logistics.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.fuel_logistics.ust_fuel_dip_telemetry import USTFuelDipTelemetryParser
from services.fuel_logistics.tanker_decanting_audit import TankerDecantingReconciler
from services.fuel_logistics.fuel_stockout_predictor import FuelStockoutPredictor


class TestFuelLogistics(unittest.TestCase):
    def test_ust_fuel_probe_telemetry(self):
        tank = USTFuelDipTelemetryParser.parse_probe_frame(
            tank_id="UST-01",
            fuel_level_mm=2100.0,
            water_level_mm=10.0,
            fuel_temp_c=25.0
        )
        self.assertEqual(tank['tank_id'], 'UST-01')
        self.assertGreater(tank['gross_volume_liters'], 20000.0)
        self.assertFalse(tank['is_water_alarm'])

    def test_ust_water_bottom_critical_alarm(self):
        tank = USTFuelDipTelemetryParser.parse_probe_frame(
            tank_id="UST-01",
            fuel_level_mm=2100.0,
            water_level_mm=30.0, # > 25mm threshold
            fuel_temp_c=25.0
        )
        self.assertTrue(tank['is_water_alarm'])
        self.assertEqual(tank['tank_health_state'], 'CRITICAL_WATER_CONTAMINATION')

    def test_tanker_decanting_shortage_audit(self):
        reconcile = TankerDecantingReconciler.reconcile_decanting(
            challan_number="CH-9842",
            invoice_liters=20000.0,
            tank_pre_dip_liters=10000.0,
            tank_post_dip_liters=29500.0 # Received 19500 (500L short = 2.5% loss > 0.15%)
        )
        self.assertTrue(reconcile['is_short_delivery_flagged'])
        self.assertEqual(reconcile['decanting_status'], 'DELIVERY_ACCEPTED_WITH_SHORTAGE_CLAIM')

    def test_fuel_stockout_prediction(self):
        stock = FuelStockoutPredictor.predict_stockout(current_inventory_liters=5000.0, avg_daily_consumption_liters=3000.0)
        self.assertTrue(stock['is_purchase_indent_required'])
        self.assertLess(stock['days_of_supply_remaining'], 2.0)


if __name__ == '__main__':
    unittest.main()
