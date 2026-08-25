"""
CityBus Enterprise Platform - Transit Standards (NeTEx, SIRI, GBFS) Tests
File: tests/test_transit_standards.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.transit_standards.netex_exporter import NeTExExporter
from services.transit_standards.siri_server import SIRIServer
from services.transit_standards.gbfs_mobility_hub import GBFSMobilityHub


class TestTransitStandards(unittest.TestCase):
    def test_netex_xml_export(self):
        routes = [{'id': 1, 'route_number': '27A', 'name': 'Corridor Route'}]
        stops = [{'id': 101, 'name': 'PNBS', 'latitude': 16.5100, 'longitude': 80.6175}]
        xml_doc = NeTExExporter.generate_netex_xml(routes, stops)
        self.assertIn('<PublicationDelivery', xml_doc)
        self.assertIn('<ScheduledStopPoint id="SP_101"', xml_doc)
        self.assertIn('<Line id="LIN_1"', xml_doc)

    def test_siri_stop_monitoring_xml(self):
        arrivals = [{'route_number': '27A', 'destination': 'Guntur', 'bus_id': 1, 'expected_arrival_iso': '2026-08-25T10:30:00'}]
        xml_siri = SIRIServer.generate_stop_monitoring_siri(101, "PNBS", arrivals)
        self.assertIn('<StopMonitoringDelivery', xml_siri)
        self.assertIn('<LineRef>27A</LineRef>', xml_siri)

    def test_gbfs_mobility_hub(self):
        gbfs = GBFSMobilityHub.get_station_status()
        self.assertEqual(gbfs['version'], '2.2')
        self.assertGreater(len(gbfs['data']['stations']), 0)
        self.assertIn('num_bikes_available', gbfs['data']['stations'][0])


if __name__ == '__main__':
    unittest.main()
