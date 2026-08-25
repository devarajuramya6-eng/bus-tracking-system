"""
CityBus Enterprise Platform - Demand Responsive Microtransit Unit Tests
File: tests/test_demand_responsive.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.demand_responsive.drts_matching_engine import DRTSMatchingEngine, DRTSPassengerRequest
from services.demand_responsive.virtual_stop_geofence import VirtualStopGeofence
from services.demand_responsive.feeder_timetable_sync import FeederTimetableSynchronizer


class TestDemandResponsiveTransit(unittest.TestCase):
    def test_drts_ride_pooling(self):
        reqs = [
            DRTSPassengerRequest("R1", 101, 16.501, 80.652, "PNBS", 420),
            DRTSPassengerRequest("R2", 102, 16.505, 80.638, "PNBS", 425)
        ]
        match = DRTSMatchingEngine.match_passengers_to_feeder_van(reqs, van_id="VAN-01", max_capacity=10)
        self.assertEqual(match['total_passengers_assigned'], 2)
        self.assertEqual(len(match['overflow_queue']), 0)

    def test_virtual_stop_geofence_clustering(self):
        snap = VirtualStopGeofence.find_nearest_safe_virtual_stop(user_lat=16.5015, user_lng=80.6515)
        self.assertIn('virtual_stop_id', snap)
        self.assertLess(snap['walking_distance_meters'], 200.0)

    def test_feeder_timetable_sync(self):
        sync = FeederTimetableSynchronizer.calculate_sync_arrival(feeder_eta_min=420, trunk_departure_min=425, trunk_route_number="27A")
        self.assertEqual(sync['transfer_status'], 'GUARANTEED_SEAMLESS_TRANSFER')
        self.assertEqual(sync['buffer_minutes'], 5)


if __name__ == '__main__':
    unittest.main()
