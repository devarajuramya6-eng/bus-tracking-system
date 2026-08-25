"""
CityBus Enterprise Platform - Maintenance Operations Unit Tests
File: tests/test_maintenance_ops.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.maintenance_ops.predictive_health_model import FleetPredictiveHealthModel
from services.maintenance_ops.spare_parts_inventory import SparePartsInventoryEngine
from services.maintenance_ops.workshop_scheduler import WorkshopBayScheduler


class TestMaintenanceOps(unittest.TestCase):
    def test_predictive_health_model(self):
        health = FleetPredictiveHealthModel.evaluate_vehicle_health(bus_id=1, odometer_km=45000.0, total_stops_served=8500)
        self.assertIn('overall_health_score', health)
        self.assertIn('brake_lining_thickness_mm', health)
        self.assertIn('tire_tread_depth_mm', health)
        self.assertGreaterEqual(health['overall_health_score'], 30)

    def test_spare_parts_eoq_and_inventory(self):
        items = SparePartsInventoryEngine.calculate_eoq_and_status()
        self.assertGreater(len(items), 0)
        self.assertIn('eoq_quantity', items[0])
        self.assertIn('is_reorder_needed', items[0])

    def test_workshop_bay_scheduler(self):
        overview = WorkshopBayScheduler.get_workshop_overview()
        self.assertGreater(overview['total_bays'], 0)
        self.assertIn('utilization_pct', overview)


if __name__ == '__main__':
    unittest.main()
