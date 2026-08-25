"""
CityBus Enterprise Platform - Transit Digital Advertising Tests
File: tests/test_transit_ads.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.transit_ads.geofenced_digital_ad_server import GeofencedAdServer
from services.transit_ads.impression_audit_beacon import AdImpressionAuditor
from services.transit_ads.audio_jingle_sponsorship_sync import AudioJingleSponsorshipSync


class TestTransitAds(unittest.TestCase):
    def test_geofenced_ad_serving(self):
        ad = GeofencedAdServer.get_ad_for_location(current_lat=16.5062, current_lng=80.6480) # Benz Circle
        self.assertTrue(ad['is_geofenced_match'])
        self.assertEqual(ad['campaign_id'], 'CAMP_MALL_01')

    def test_proof_of_play_impression_audit(self):
        pop = AdImpressionAuditor.record_play_event(
            campaign_id="CAMP_MALL_01",
            bus_number="AP16-001",
            duration_sec=15,
            passenger_count=38
        )
        self.assertTrue(pop['is_billing_certified'])
        self.assertEqual(pop['verified_impressions_count'], 38)
        self.assertEqual(len(pop['proof_of_play_signature']), 16)

    def test_audio_jingle_sponsorship_sync(self):
        sync = AudioJingleSponsorshipSync.get_sponsored_audio_tail(
            stop_name="Benz Circle",
            stops_since_last_sponsor=4
        )
        self.assertTrue(sync['is_sponsored'])
        self.assertEqual(sync['sponsor_name'], 'Trendset Mall')


if __name__ == '__main__':
    unittest.main()
