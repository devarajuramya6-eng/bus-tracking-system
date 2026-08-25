"""
CityBus Enterprise Platform - Micro-Mobility & Shared Bike Feeder Tests
File: tests/test_micromobility.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.micromobility.e_scooter_geofencing import MicroMobilityGeofenceEngine
from services.micromobility.docking_station_rebalancer import DockingStationRebalancer
from services.micromobility.single_ticket_intermodal_clearing import IntermodalMicroTicketClearing


class TestMicroMobility(unittest.TestCase):
    def test_geofence_no_ride_zone(self):
        eval_gf = MicroMobilityGeofenceEngine.evaluate_vehicle_position(lat=16.5140, lng=80.6050, current_speed_kmh=15.0)
        self.assertEqual(eval_gf['active_rule'], 'NO_RIDE_ZONE')
        self.assertFalse(eval_gf['motor_throttle_enabled'])

    def test_dock_rebalancing_audit(self):
        stations = [
            {'id': 1, 'name': 'Station A', 'capacity': 20, 'available_bikes': 1}, # Starved
            {'id': 2, 'name': 'Station B', 'capacity': 20, 'available_bikes': 19}  # Overflowing
        ]
        audit = DockingStationRebalancer.audit_dock_inventory(stations)
        self.assertEqual(audit['starved_stations_count'], 1)
        self.assertEqual(audit['overflowing_stations_count'], 1)
        self.assertTrue(audit['rebalancing_truck_dispatch_recommended'])

    def test_intermodal_single_ticket_clearing(self):
        pass_ticket = IntermodalMicroTicketClearing.create_intermodal_pass(
            user_id=101,
            bus_fare_inr=25.0,
            bike_duration_min=10,
            bike_rate_per_min=1.0 # 10 INR
        ) # Gross 35, -5 discount = 30 INR
        self.assertEqual(pass_ticket['total_amount_inr'], 30.0)
        self.assertEqual(pass_ticket['multimodal_transfer_discount_inr'], 5.0)


if __name__ == '__main__':
    unittest.main()
