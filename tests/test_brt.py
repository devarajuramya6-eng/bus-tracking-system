"""
CityBus Enterprise Platform - BRT Corridor & Traffic Signal Priority Tests
File: tests/test_brt.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.brt.transit_signal_priority import TransitSignalPriorityEngine
from services.brt.bus_lane_enforcement import DedicatedLaneEnforcement


class TestBRTAndSignalPriority(unittest.TestCase):
    def test_transit_signal_priority_delayed_bus(self):
        req = TransitSignalPriorityEngine.evaluate_tsp_request(
            bus_id=10,
            bus_lat=16.5020,
            bus_lng=80.6475,
            speed_kmh=32.0,
            occupancy=42,
            delay_minutes=4.5,
            junction_id="JNC-BENZ-01"
        )
        self.assertTrue(req['tsp_granted'])
        self.assertEqual(req['action'], 'REQUEST_GREEN_EXTENSION_12S')

    def test_dedicated_lane_enforcement_violation(self):
        challan = DedicatedLaneEnforcement.generate_violation_evidence(
            bus_id=14,
            detected_plate="AP 16 AB 9988",
            vehicle_type="Private SUV",
            lat=16.5020,
            lng=80.6475,
            corridor_name="MG Road BRT Transit Corridor"
        )
        self.assertIn('violation_id', challan)
        self.assertEqual(challan['penalty_fine_inr'], 2000.0)
        self.assertEqual(challan['violator_license_plate'], "AP 16 AB 9988")


if __name__ == '__main__':
    unittest.main()
