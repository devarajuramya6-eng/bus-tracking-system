"""
CityBus Enterprise Platform - GTFS-Realtime Protocol Buffer Feed Tests
File: tests/test_gtfs_rt_feeds.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.open_data.gtfs_realtime_trip_updates import GTFSTripUpdatesFeed
from services.open_data.gtfs_realtime_alerts_feed import GTFSServiceAlertsFeed
from services.open_data.gtfs_realtime_vehicle_feed import GTFSVehiclePositionsFeed


class TestGTFSRealtimeFeeds(unittest.TestCase):
    def test_trip_updates_feed_generation(self):
        updates = [{
            'trip_id': 'TRIP_101',
            'route_id': '27A',
            'stops': [{'stop_id': 101, 'delay_seconds': 120, 'stop_sequence': 1}]
        }]
        feed = GTFSTripUpdatesFeed.build_feed(updates)
        self.assertEqual(feed['header']['gtfs_realtime_version'], '2.0')
        self.assertEqual(len(feed['entity']), 1)
        self.assertIn('trip_update', feed['entity'][0])

    def test_service_alerts_feed_generation(self):
        alerts = [{
            'id': 'ALT-01',
            'route_id': '27A',
            'cause': 'CONSTRUCTION',
            'effect': 'DETOUR',
            'title_en': 'Corridor Detour',
            'desc_en': 'Diversion via flyover'
        }]
        feed = GTFSServiceAlertsFeed.build_feed(alerts)
        self.assertEqual(len(feed['entity']), 1)
        self.assertIn('alert', feed['entity'][0])

    def test_vehicle_positions_feed_generation(self):
        vehicles = [{
            'id': 1,
            'bus_number': 'AP16-001',
            'latitude': 16.5062,
            'longitude': 80.6480,
            'speed': 35.0,
            'heading': 90.0,
            'occupancy': 32
        }]
        feed = GTFSVehiclePositionsFeed.build_feed(vehicles)
        self.assertEqual(len(feed['entity']), 1)
        self.assertEqual(feed['entity'][0]['vehicle']['occupancy_status'], 'FEW_SEATS_AVAILABLE')


if __name__ == '__main__':
    unittest.main()
