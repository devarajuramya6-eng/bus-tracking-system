"""
CityBus Enterprise Platform - Passenger Information System (PIS) Unit Tests
File: tests/test_pis.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.pis.led_destination_display import LEDDestinationDisplay
from services.pis.audio_announcement_generator import AudioAnnouncementGenerator
from services.pis.gtfs_realtime_generator import GTFSRealtimeFeedGenerator


class TestPassengerInformationSystem(unittest.TestCase):
    def test_led_destination_display_payload(self):
        payload = LEDDestinationDisplay.get_display_payload("27A", next_stop_name="Mangalagiri AIIMS")
        self.assertEqual(payload['route_number'], '27A')
        self.assertIn('line_1_telugu', payload['front_display'])
        self.assertIn('line_1_english', payload['front_display'])

    def test_audio_announcement_generator(self):
        audio = AudioAnnouncementGenerator.generate_next_stop_announcement("బెంజ్ సర్కిల్", "Benz Circle", "27A")
        self.assertIn('scripts', audio)
        self.assertIn('te-IN', audio['scripts'])
        self.assertIn('en-IN', audio['scripts'])

    def test_gtfs_realtime_vehicle_positions(self):
        buses = [
            {'id': 1, 'route_id': 1, 'latitude': 16.5062, 'longitude': 80.6480, 'speed': 35.0, 'heading': 90.0, 'occupancy': 28}
        ]
        feed = GTFSRealtimeFeedGenerator.generate_vehicle_positions_feed(buses)
        self.assertEqual(feed['header']['gtfs_realtime_version'], '2.0')
        self.assertEqual(len(feed['entity']), 1)
        self.assertIn('position', feed['entity'][0]['vehicle'])


if __name__ == '__main__':
    unittest.main()
